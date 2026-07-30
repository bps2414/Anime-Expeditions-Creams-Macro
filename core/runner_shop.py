"""Daily Gold Shop automation executed only from lobby-safe runner boundaries."""

import threading
import time

from . import auto_shop
from . import auto_shop_vision
from . import camera
from . import keys
from . import vision
from . import window as wm


SHOP_KEY = "gold_shop"
SHOP_NAV_TIMEOUT = 10.0
SHOP_LOAD_TIMEOUT = 60.0
SHOP_OPEN_TIMEOUT = 10.0
SHOP_MODAL_TIMEOUT = 4.0
SHOP_MODAL_CLOSE_TIMEOUT = 5.0
SHOP_SCROLL_AMOUNT = -120
SHOP_SCROLL_ATTEMPTS = 8
SHOP_LIST_CENTER = (545, 410)
SHOP_LIST_VIEWPORT = (398, 218, 308, 362)
SHOP_SETTLE_DELAY = 0.6
SHOP_CAPTURE_INTERVAL = 0.12

_TERMINAL_ITEM_STATUSES = {
    auto_shop.STATUS_COMPLETED,
    auto_shop.STATUS_OUT_OF_STOCK,
    auto_shop.STATUS_FAILED_TODAY,
}


class ShopOps:
    def _auto_shop_settings(self) -> dict:
        if self._get_auto_shop_settings is None:
            return {}
        try:
            return self._get_auto_shop_settings() or {}
        except Exception as exc:
            self._log(f"[Shop] Couldn't read Auto Shop settings: {exc}")
            return {}

    def _auto_shop_due_items(self, settings=None) -> list:
        settings = settings or self._auto_shop_settings()
        if not settings.get("enabled"):
            return []
        shop = (settings.get("shops") or {}).get(SHOP_KEY) or {}
        if not shop.get("enabled"):
            return []
        if (shop.get("state") or {}).get("status") == auto_shop.STATUS_FAILED_TODAY:
            return []
        return [
            item
            for item in (shop.get("items") or [])
            if item.get("enabled")
            and (item.get("state") or {}).get("status") not in _TERMINAL_ITEM_STATUSES
        ]

    def _auto_shop_wants_in(self) -> bool:
        """Return whether the Gold Shop has any actionable configured item."""
        return bool(self._auto_shop_due_items())

    def _shop_save_item_state(self, shop_key: str, item_key: str, state: dict) -> None:
        if self._save_auto_shop_item_state is None:
            return
        try:
            self._save_auto_shop_item_state(shop_key, item_key, state)
        except Exception as exc:
            self._log(f"[Shop] Couldn't save {item_key} state: {exc}")

    def _shop_save_shop_state(self, shop_key: str, state: dict) -> None:
        if self._save_auto_shop_shop_state is None:
            return
        try:
            self._save_auto_shop_shop_state(shop_key, state)
        except Exception as exc:
            self._log(f"[Shop] Couldn't save {shop_key} state: {exc}")

    @staticmethod
    def _shop_state_period(state: dict) -> str:
        return str((state or {}).get("period") or auto_shop.current_auto_shop_period())

    @staticmethod
    def _shop_region_is_visible(region: tuple) -> bool:
        x, y, width, height = region
        view_x, view_y, view_width, view_height = SHOP_LIST_VIEWPORT
        return (
            x >= view_x
            and y >= view_y
            and x + width <= view_x + view_width
            and y + height <= view_y + view_height
        )

    def _shop_find_item(
            self, hwnd, item: dict, stop_event: threading.Event):
        template = auto_shop.item_definition(item["key"])["template"]
        for attempt in range(SHOP_SCROLL_ATTEMPTS + 1):
            if self._checkpoint(stop_event):
                return None
            try:
                match = vision.find_image(hwnd, template)
            except vision.TemplateNotFound as exc:
                self._log(f"[Shop] {exc}")
                return None
            if match is not None:
                stock_region = auto_shop_vision.stock_status_region_from_item_match(match)
                buy_region = auto_shop_vision.initial_buy_region_from_item_match(match)
                if (
                        self._shop_region_is_visible(stock_region)
                        and self._shop_region_is_visible(buy_region)):
                    return match
            if attempt == SHOP_SCROLL_ATTEMPTS:
                break
            x, y = vision.ref_to_screen(hwnd, *SHOP_LIST_CENTER)
            self._mouse.move_to(x, y)
            self._mouse.nudge()
            self._mouse.scroll(SHOP_SCROLL_AMOUNT)
            time.sleep(SHOP_SETTLE_DELAY)
        self._log(f'[Shop] "{item["name"]}" was not found after scrolling the full list.')
        return None

    def _shop_read_observation(
            self, hwnd, item: dict, item_match: dict,
            stop_event: threading.Event) -> dict:
        status_region = auto_shop_vision.stock_status_region_from_item_match(item_match)
        try:
            out_of_stock = vision.find_image(
                hwnd,
                auto_shop.AUTO_SHOP_UI_TEMPLATES["out_of_stock"],
                region=status_region,
            ) is not None
        except vision.TemplateNotFound:
            out_of_stock = False

        stock_region = auto_shop_vision.stock_region_from_item_match(item_match)
        crops = []
        for index in range(3):
            if self._checkpoint(stop_event):
                break
            crop = vision.capture_game_bgr(hwnd, stock_region)
            if crop is not None and crop.size:
                crops.append(crop)
            if index < 2:
                time.sleep(SHOP_CAPTURE_INTERVAL)

        signature = (
            auto_shop.build_stock_signature(crops[-1])
            if crops else ""
        )
        if out_of_stock:
            return {
                "left": 0,
                "signature": signature,
                "out_of_stock": True,
            }
        daily_maximum = int(item["daily_maximum"])
        left = (
            auto_shop_vision.read_left_consensus(crops, daily_maximum)
            if len(crops) == 3 else None
        )
        return {
            "left": left,
            "signature": signature,
            "out_of_stock": False,
        }

    def _shop_open_purchase_modal(
            self, hwnd, item_match: dict, stop_event: threading.Event):
        region = auto_shop_vision.initial_buy_region_from_item_match(item_match)
        try:
            buy_match = vision.find_image(
                hwnd,
                auto_shop.AUTO_SHOP_UI_TEMPLATES["buy"],
                region=region,
            )
        except vision.TemplateNotFound as exc:
            self._log(f"[Shop] {exc}")
            return None
        if buy_match is None:
            self._log(
                "[Shop] The enabled Buy button was not detected inside "
                "the visible item card."
            )
            return None
        vision.click_match(self._mouse, hwnd, buy_match)
        try:
            cancel_match = vision.wait_for_image(
                hwnd,
                auto_shop.AUTO_SHOP_UI_TEMPLATES["cancel"],
                timeout=SHOP_MODAL_TIMEOUT,
                stop_event=stop_event,
            )
        except vision.TemplateNotFound as exc:
            self._log(f"[Shop] {exc}")
            return None
        if cancel_match is None and not self._checkpoint(stop_event):
            self._log(
                "[Shop] Buy was clicked, but the purchase modal did not open; "
                "the button may be disabled by insufficient Gold."
            )
        return cancel_match

    def _shop_configure_amount(
            self, hwnd, cancel_match: dict, target, amount: int,
            stop_event: threading.Event) -> bool:
        if str(target).lower() == "max":
            region = auto_shop_vision.amount_toggle_region_from_cancel(cancel_match)
            try:
                min_match = vision.find_image(
                    hwnd,
                    auto_shop.AUTO_SHOP_UI_TEMPLATES["amount_min"],
                    region=region,
                )
                if min_match is not None:
                    return True
                max_match = vision.find_image(
                    hwnd,
                    auto_shop.AUTO_SHOP_UI_TEMPLATES["amount_max"],
                    region=region,
                )
            except vision.TemplateNotFound as exc:
                self._log(f"[Shop] {exc}")
                return False
            if max_match is None:
                self._log("[Shop] Neither Max nor Min was detected in the amount modal.")
                return False
            vision.click_match(self._mouse, hwnd, max_match)
            time.sleep(SHOP_SETTLE_DELAY)
            if self._checkpoint(stop_event):
                return False
            try:
                return vision.find_image(
                    hwnd,
                    auto_shop.AUTO_SHOP_UI_TEMPLATES["amount_min"],
                    region=region,
                ) is not None
            except vision.TemplateNotFound:
                return False

        region = auto_shop_vision.amount_input_region_from_cancel(cancel_match)
        x, y, width, height = region
        screen_x, screen_y = vision.ref_to_screen(
            hwnd,
            x + width // 2,
            y + height // 2,
        )
        self._mouse.double_click(screen_x, screen_y)
        time.sleep(0.15)
        self._keyboard.combo(keys.VK_CONTROL, ord("A"))
        self._keyboard.tap(keys.VK_DELETE)
        self._keyboard.type_text(str(int(amount)))
        time.sleep(SHOP_SETTLE_DELAY)
        return not self._checkpoint(stop_event)

    def _shop_cancel_modal(self, hwnd, cancel_match: dict) -> None:
        x, y = auto_shop_vision.cancel_click_point(cancel_match)
        screen_x, screen_y = vision.ref_to_screen(hwnd, x, y)
        self._mouse.click(screen_x, screen_y)

    def _shop_confirm_purchase(
            self, hwnd, cancel_match: dict, stop_event: threading.Event) -> bool:
        region = auto_shop_vision.final_buy_region_from_cancel(cancel_match)
        x, y, width, height = region
        screen_x, screen_y = vision.ref_to_screen(
            hwnd,
            x + width // 2,
            y + height // 2,
        )
        self._mouse.click(screen_x, screen_y)
        if self._checkpoint(stop_event):
            return False
        if self._wait_for_image_gone(
                hwnd,
                (auto_shop.AUTO_SHOP_UI_TEMPLATES["cancel"],),
                SHOP_MODAL_CLOSE_TIMEOUT,
                stop_event,
        ):
            return True
        self._shop_cancel_modal(hwnd, cancel_match)
        return False

    @staticmethod
    def _shop_observation_changed(before: dict, after: dict):
        before_signature = str(before.get("signature") or "")
        after_signature = str(after.get("signature") or "")
        if not before_signature or not after_signature:
            return None
        try:
            return auto_shop_vision.stock_visual_changed(
                before_signature,
                after_signature,
            )
        except ValueError:
            return None

    def _shop_state_from_observation(
            self, item: dict, state: dict, observation: dict) -> dict:
        current = auto_shop.normalize_item_state(
            state,
            self._shop_state_period(state),
        )
        current["last_known_left"] = observation.get("left")
        current["stock_signature"] = str(observation.get("signature") or "")
        current["verification"] = None
        if observation.get("out_of_stock"):
            current["status"] = auto_shop.STATUS_OUT_OF_STOCK
        else:
            plan = auto_shop.calculate_purchase_plan(
                item["key"],
                item["target"],
                int(observation["left"]),
            )
            current["status"] = plan["status"]
        return current

    def _shop_verify_pending(
            self, item: dict, state: dict, observation: dict):
        verification = state.get("verification") or {}
        if observation.get("out_of_stock"):
            return self._shop_state_from_observation(item, state, observation), True
        if observation.get("left") is None:
            return state, False
        before = {
            "left": verification.get("before_left"),
            "signature": verification.get("before_signature"),
        }
        result = auto_shop.classify_stock_verification(
            before.get("left"),
            observation.get("left"),
            self._shop_observation_changed(before, observation),
        )
        if result == auto_shop.VERIFICATION_PROGRESS:
            return self._shop_state_from_observation(item, state, observation), True
        if result == auto_shop.VERIFICATION_UNCHANGED:
            ready = auto_shop.normalize_item_state(
                state,
                self._shop_state_period(state),
            )
            ready["status"] = auto_shop.STATUS_PENDING
            ready["verification"] = None
            ready["last_known_left"] = observation["left"]
            ready["stock_signature"] = observation.get("signature") or ""
            return ready, True
        return state, False

    def _shop_process_item(
            self, hwnd, shop_key: str, item: dict,
            stop_event: threading.Event) -> None:
        item_key = item["key"]
        period = self._shop_state_period(item.get("state") or {})
        state = auto_shop.normalize_item_state(item.get("state"), period)
        match = self._shop_find_item(hwnd, item, stop_event)
        if match is None:
            self._shop_save_item_state(
                shop_key,
                item_key,
                auto_shop.record_item_failure(state, period),
            )
            return

        observation = self._shop_read_observation(
            hwnd,
            item,
            match,
            stop_event,
        )
        if state["status"] == auto_shop.STATUS_PENDING_VERIFICATION:
            state, resolved = self._shop_verify_pending(item, state, observation)
            self._shop_save_item_state(shop_key, item_key, state)
            if not resolved or state["status"] != auto_shop.STATUS_PENDING:
                return

        if observation.get("out_of_stock"):
            self._shop_save_item_state(
                shop_key,
                item_key,
                self._shop_state_from_observation(item, state, observation),
            )
            return
        if observation.get("left") is None:
            self._shop_save_item_state(
                shop_key,
                item_key,
                auto_shop.record_item_failure(state, period),
            )
            return

        plan = auto_shop.calculate_purchase_plan(
            item_key,
            item["target"],
            int(observation["left"]),
        )
        if plan["status"] != auto_shop.STATUS_PENDING:
            self._shop_save_item_state(
                shop_key,
                item_key,
                self._shop_state_from_observation(item, state, observation),
            )
            return

        cancel_match = self._shop_open_purchase_modal(
            hwnd,
            match,
            stop_event,
        )
        if cancel_match is None:
            self._log(
                f'[Shop] "{item["name"]}" purchase was not started safely.'
            )
            self._shop_save_item_state(
                shop_key,
                item_key,
                auto_shop.record_item_failure(state, period),
            )
            return
        if not self._shop_configure_amount(
                hwnd,
                cancel_match,
                item["target"],
                plan["pending_amount"],
                stop_event,
        ):
            self._shop_cancel_modal(hwnd, cancel_match)
            self._shop_save_item_state(
                shop_key,
                item_key,
                auto_shop.record_item_failure(state, period),
            )
            return

        pending = auto_shop.normalize_item_state(state, period)
        pending["status"] = auto_shop.STATUS_PENDING_VERIFICATION
        pending["last_known_left"] = observation["left"]
        pending["stock_signature"] = observation.get("signature") or ""
        pending["verification"] = {
            "before_left": observation["left"],
            "before_signature": observation.get("signature") or "",
        }
        self._shop_save_item_state(shop_key, item_key, pending)

        if not self._shop_confirm_purchase(hwnd, cancel_match, stop_event):
            if not stop_event.is_set():
                self._shop_save_item_state(
                    shop_key,
                    item_key,
                    auto_shop.record_item_failure(pending, period),
                )
            return

        refreshed_match = self._shop_find_item(hwnd, item, stop_event)
        if refreshed_match is None:
            return
        after = self._shop_read_observation(
            hwnd,
            item,
            refreshed_match,
            stop_event,
        )
        result = auto_shop.classify_stock_verification(
            observation["left"],
            after.get("left"),
            self._shop_observation_changed(observation, after),
            out_of_stock=bool(after.get("out_of_stock")),
        )
        if result in (
                auto_shop.VERIFICATION_PROGRESS,
                auto_shop.VERIFICATION_OUT_OF_STOCK):
            final_state = self._shop_state_from_observation(item, pending, after)
            self._shop_save_item_state(shop_key, item_key, final_state)
        elif result == auto_shop.VERIFICATION_UNCHANGED:
            self._shop_save_item_state(
                shop_key,
                item_key,
                auto_shop.record_item_failure(pending, period),
            )

    def _shop_enter_gold_shop(
            self, hwnd, stop_event: threading.Event) -> bool:
        for name, action in (
            ("nav_area", "Opening Areas..."),
            (auto_shop.AUTO_SHOP_UI_TEMPLATES["navigation"], "Opening Shop..."),
            (auto_shop.AUTO_SHOP_UI_TEMPLATES["destination"], "Entering Gold Shop..."),
        ):
            self._set_status(action=action)
            if self._click_found_image(
                    hwnd,
                    name,
                    SHOP_NAV_TIMEOUT,
                    stop_event,
            ) is None:
                return False
            if self._checkpoint(stop_event):
                return False
            time.sleep(SHOP_SETTLE_DELAY)

        if not self._wait_for_image_gone(
                hwnd,
                ("nav_play",),
                SHOP_NAV_TIMEOUT,
                stop_event,
        ):
            self._log("[Shop] Gold Shop teleport never started.")
            return False
        self._set_status(action="Loading Gold Shop...")
        try:
            loaded = vision.wait_for_image(
                hwnd,
                "nav_play",
                timeout=SHOP_LOAD_TIMEOUT,
                stop_event=stop_event,
            )
        except vision.TemplateNotFound:
            loaded = None
        if loaded is None:
            return False
        if not wm.activate_window(hwnd):
            self._log("[Shop] Couldn't confirm Roblox focus before opening Gold Shop.")
            return False
        time.sleep(0.5)
        camera.tilt_camera_top_down(self._mouse, hwnd)
        self._keyboard.tap(ord("E"))
        self._set_status(action="Selecting Gold Shop...")
        if self._click_found_image(
                hwnd,
                auto_shop.AUTO_SHOP_UI_TEMPLATES["shop_tab"],
                SHOP_OPEN_TIMEOUT,
                stop_event,
        ) is None:
            self._log("[Shop] Couldn't find the Gold Shop tab after pressing E.")
            return False
        if self._checkpoint(stop_event):
            return False
        time.sleep(SHOP_SETTLE_DELAY)
        try:
            opened = vision.wait_for_image(
                hwnd,
                auto_shop.item_definition("cursed_boba")["template"],
                timeout=SHOP_OPEN_TIMEOUT,
                stop_event=stop_event,
            )
        except vision.TemplateNotFound:
            opened = None
        return opened is not None

    def _run_auto_shop(
            self, hwnd, stop_event: threading.Event) -> None:
        settings = self._auto_shop_settings()
        due_items = self._auto_shop_due_items(settings)
        if not due_items:
            return
        shop = settings["shops"][SHOP_KEY]
        period = self._shop_state_period(shop.get("state") or {})
        self._log(f"[Shop] Starting Auto Shop for {len(due_items)} item(s).")
        self._set_status(
            current_task="Auto Shop",
            action="Preparing Gold Shop...",
            mode="shop",
            map="-",
            stage="-",
            difficulty="-",
            macro="-",
            play_mode="-",
        )
        wm.show_window(hwnd)
        if not wm.activate_window(hwnd):
            self._log("[Shop] Couldn't confirm Roblox took focus.")
            return
        time.sleep(0.5)
        if not self._ensure_lobby(hwnd, stop_event):
            return
        if not self._shop_enter_gold_shop(hwnd, stop_event):
            failed = auto_shop.record_navigation_failure(
                shop.get("state"),
                period,
            )
            self._shop_save_shop_state(SHOP_KEY, failed)
            if not stop_event.is_set():
                self._recover_to_lobby(hwnd, stop_event)
            return

        self._shop_save_shop_state(
            SHOP_KEY,
            auto_shop.fresh_shop_state(period),
        )
        for item in due_items:
            if self._checkpoint(stop_event):
                return
            self._set_status(action=f'Checking {item["name"]}...')
            self._shop_process_item(hwnd, SHOP_KEY, item, stop_event)

        if not stop_event.is_set():
            try:
                close_match = vision.find_image(hwnd, "nav_closeui")
            except vision.TemplateNotFound:
                close_match = None
            if close_match is not None:
                vision.click_match(self._mouse, hwnd, close_match)
                time.sleep(SHOP_SETTLE_DELAY)
            self._log("[Shop] Auto Shop pass finished. Returning to the lobby.")
            self._recover_to_lobby(hwnd, stop_event)

    def _run_auto_shop_if_due(
            self, hwnd, stop_event: threading.Event) -> None:
        if self._auto_shop_wants_in():
            self._run_auto_shop(hwnd, stop_event)
