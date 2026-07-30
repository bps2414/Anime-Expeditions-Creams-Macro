import threading
from unittest.mock import MagicMock

import numpy as np
import pytest

from core import auto_shop
from core import runner_shop
from core.runner import MacroRunner


def _runner(saved_items):
    return MacroRunner(
        MagicMock(),
        MagicMock(),
        MagicMock(),
        save_auto_shop_item_state=lambda shop, item, state: saved_items.append(
            (shop, item, state)
        ),
    )


def _item(target=5):
    return {
        "key": "cursed_boba",
        "name": "Cursed Boba",
        "daily_maximum": 50,
        "target": target,
        "state": auto_shop.fresh_item_state("2026-07-30"),
    }


def test_visible_numeric_purchase_remains_due_without_reading_stock(monkeypatch):
    """A numeric purchase must repeat on later passes until the card is terminal."""
    saved_items = []
    runner = _runner(saved_items)
    cancel = {"x": 579, "y": 420, "w": 181, "h": 28}
    item = _item(target=5)
    runner._shop_read_observation = MagicMock(
        side_effect=AssertionError("The no-OCR path must not read stock")
    )
    monkeypatch.setattr(runner, "_shop_find_terminal_label", lambda *_args: None)
    monkeypatch.setattr(runner, "_shop_open_purchase_modal", lambda *_args: cancel)
    monkeypatch.setattr(runner, "_shop_configure_amount", lambda *_args: True)
    monkeypatch.setattr(runner, "_shop_confirm_purchase", lambda *_args: True)

    runner._shop_process_visible_item(
        1,
        "gold_shop",
        item,
        {"x": 429, "y": 245, "w": 61, "h": 55},
        threading.Event(),
    )

    runner._shop_read_observation.assert_not_called()
    assert saved_items[-1][2]["status"] == auto_shop.STATUS_PENDING
    assert saved_items[-1][2]["verification"] is None


def test_visible_max_purchase_is_completed_for_the_current_day(monkeypatch):
    saved_items = []
    runner = _runner(saved_items)
    cancel = {"x": 579, "y": 420, "w": 181, "h": 28}
    item = _item(target="max")
    monkeypatch.setattr(runner, "_shop_find_terminal_label", lambda *_args: None)
    monkeypatch.setattr(runner, "_shop_open_purchase_modal", lambda *_args: cancel)
    monkeypatch.setattr(runner, "_shop_configure_amount", lambda *_args: True)
    monkeypatch.setattr(runner, "_shop_confirm_purchase", lambda *_args: True)

    runner._shop_process_visible_item(
        1,
        "gold_shop",
        item,
        {"x": 429, "y": 245, "w": 61, "h": 55},
        threading.Event(),
    )

    assert saved_items[-1][2]["status"] == auto_shop.STATUS_COMPLETED


def test_visible_purchase_with_uncertain_modal_requires_a_manual_today_reset(monkeypatch):
    """A final Buy that does not close must not restart the shop every task."""
    saved_items = []
    runner = _runner(saved_items)
    cancel = {"x": 579, "y": 420, "w": 181, "h": 28}
    item = _item(target="max")
    monkeypatch.setattr(runner, "_shop_find_terminal_label", lambda *_args: None)
    monkeypatch.setattr(runner, "_shop_open_purchase_modal", lambda *_args: cancel)
    monkeypatch.setattr(runner, "_shop_configure_amount", lambda *_args: True)
    monkeypatch.setattr(runner, "_shop_confirm_purchase", lambda *_args: False)

    runner._shop_process_visible_item(
        1,
        "gold_shop",
        item,
        {"x": 429, "y": 245, "w": 61, "h": 55},
        threading.Event(),
    )

    assert saved_items[-1][2]["status"] == auto_shop.STATUS_FAILED_TODAY


def test_visible_item_lookup_does_not_scroll_when_the_card_is_clipped(monkeypatch):
    """Row alignment owns scrolling, so an item miss cannot move later cards."""
    runner = _runner([])
    item = _item()
    clipped = {"x": 429, "y": 445, "w": 61, "h": 55}
    monkeypatch.setattr(runner, "_checkpoint", lambda _stop: False)
    monkeypatch.setattr(
        "core.runner_shop.vision.find_image",
        lambda *_args, **_kwargs: clipped,
    )

    assert runner._shop_find_visible_item(1, item, threading.Event()) is None
    runner._mouse.scroll.assert_not_called()


def test_stat_lock_row_alignment_forces_bottom_before_searching(monkeypatch):
    """Stat Lock must not be clicked from a partially scrolled Bottom view."""
    runner = _runner([])
    item = {
        **_item(),
        "key": "stat_lock",
        "name": "Stat Lock",
        "daily_maximum": 10,
    }
    events = []
    runner._mouse.scroll.side_effect = lambda amount: events.append(("scroll", amount))
    monkeypatch.setattr(runner, "_checkpoint", lambda _stop: False)
    monkeypatch.setattr(
        "core.runner_shop.vision.find_image",
        lambda *_args, **_kwargs: events.append(("find", None)) or {
            "x": 429, "y": 325, "w": 61, "h": 55,
        },
    )
    monkeypatch.setattr(
        "core.runner_shop.vision.ref_to_screen",
        lambda _hwnd, x, y: (x, y),
    )
    monkeypatch.setattr("core.runner_shop.time.sleep", lambda _seconds: None)

    assert runner._shop_align_visible_row(
        1,
        [item],
        threading.Event(),
        force_bottom=True,
    )
    assert events[0] == ("scroll", runner_shop.SHOP_BOTTOM_SCROLL_AMOUNT)
    assert events[-1] == ("find", None)


def test_no_ocr_sweep_resets_once_then_keeps_a_single_forward_item_order(monkeypatch):
    """The sweep must not call the legacy reset-per-item finder."""
    runner = _runner([])
    items = [
        {**_item(), "key": "stat_lock", "name": "Stat Lock", "daily_maximum": 10},
        {**_item(), "key": "frown_fruit", "name": "Frown Fruit", "daily_maximum": 100},
        _item(),
    ]
    found = []
    processed = []
    runner._shop_find_item = MagicMock(
        side_effect=AssertionError("The legacy finder resets the list per item")
    )
    monkeypatch.setattr(runner, "_checkpoint", lambda _stop: False)
    monkeypatch.setattr(
        runner,
        "_shop_align_visible_row",
        lambda *_args, **_kwargs: True,
    )
    monkeypatch.setattr(
        runner,
        "_shop_find_visible_item",
        lambda _hwnd, item, _stop: found.append(item["key"]) or {
            "x": 429, "y": 325, "w": 61, "h": 55,
        },
    )
    monkeypatch.setattr(
        runner,
        "_shop_process_visible_item",
        lambda _hwnd, _shop, item, _match, _stop: processed.append(item["key"]),
    )
    monkeypatch.setattr(
        "core.runner_shop.vision.ref_to_screen",
        lambda _hwnd, x, y: (x, y),
    )
    monkeypatch.setattr("core.runner_shop.time.sleep", lambda _seconds: None)

    runner._shop_run_no_ocr_sweep(1, "gold_shop", items, threading.Event())

    assert found == ["cursed_boba", "frown_fruit", "stat_lock"]
    assert processed == found
    assert [call.args for call in runner._mouse.scroll.call_args_list] == [
        (runner_shop.SHOP_SCROLL_RESET_AMOUNT,),
    ]


def test_failed_item_match_does_not_scroll_past_the_following_row(monkeypatch):
    """One missing card must not consume the scroll budget for later cards."""
    runner = _runner([])
    items = [
        _item(),
        {**_item(), "key": "red_flower", "name": "Red Flower", "daily_maximum": 75},
        {**_item(), "key": "frown_fruit", "name": "Frown Fruit", "daily_maximum": 100},
        {
            **_item(),
            "key": "delicious_pie",
            "name": "Delicious Pie",
            "daily_maximum": 125,
        },
    ]
    row = 0
    processed = []

    def scroll(amount):
        nonlocal row
        row = 0 if amount > 0 else min(5, row + 1)

    visible_rows = {
        "shop_cursed_boba": 0,
        "shop_red_flower": None,
        "shop_frown_fruit": 1,
        "shop_delicious_pie": 1,
    }

    def find_image(_hwnd, template, **_kwargs):
        if visible_rows[template] != row:
            return None
        return {"x": 429, "y": 325, "w": 61, "h": 55, "cx": 459, "cy": 352}

    runner._mouse.scroll.side_effect = scroll
    monkeypatch.setattr(runner, "_checkpoint", lambda _stop: False)
    monkeypatch.setattr("core.runner_shop.vision.find_image", find_image)
    monkeypatch.setattr(
        runner,
        "_shop_process_visible_item",
        lambda _hwnd, _shop, item, _match, _stop: processed.append(item["key"]),
    )
    monkeypatch.setattr(
        "core.runner_shop.vision.ref_to_screen",
        lambda _hwnd, x, y: (x, y),
    )
    monkeypatch.setattr("core.runner_shop.time.sleep", lambda _seconds: None)

    runner._shop_run_no_ocr_sweep(1, "gold_shop", items, threading.Event())

    assert processed == ["cursed_boba", "frown_fruit", "delicious_pie"]
    assert row == 1


def test_auto_shop_run_delegates_enabled_items_to_the_no_ocr_sweep(monkeypatch):
    """The public runner path must not retain the old OCR item processor."""
    item = _item()
    item["enabled"] = True
    settings = {
        "enabled": True,
        "shops": {
            "gold_shop": {
                "enabled": True,
                "state": auto_shop.fresh_shop_state("2026-07-30"),
                "items": [item],
            },
        },
    }
    runner = MacroRunner(
        MagicMock(),
        MagicMock(),
        MagicMock(),
        get_auto_shop_settings=lambda: settings,
    )
    dispatched = []
    monkeypatch.setattr("core.runner_shop.wm.show_window", lambda _hwnd: None)
    monkeypatch.setattr("core.runner_shop.wm.activate_window", lambda _hwnd: True)
    monkeypatch.setattr(runner, "_ensure_lobby", lambda *_args: True)
    monkeypatch.setattr(runner, "_shop_enter_gold_shop", lambda *_args: True)
    monkeypatch.setattr(
        runner,
        "_shop_run_no_ocr_sweep",
        lambda _hwnd, shop, items, _stop: dispatched.append((shop, items)),
    )
    runner._shop_process_item = MagicMock(
        side_effect=AssertionError("The OCR processor must not run")
    )
    monkeypatch.setattr("core.runner_shop.vision.find_image", lambda *_args, **_kwargs: None)
    monkeypatch.setattr("core.runner_shop.time.sleep", lambda _seconds: None)

    runner._run_auto_shop(1, threading.Event())

    assert dispatched == [("gold_shop", [item])]


def test_public_auto_shop_run_never_reaches_stock_ocr(monkeypatch):
    """The runner integration must retain the no-OCR guarantee after refactors."""
    item = _item()
    item["enabled"] = True
    settings = {
        "enabled": True,
        "shops": {
            "gold_shop": {
                "enabled": True,
                "state": auto_shop.fresh_shop_state("2026-07-30"),
                "items": [item],
            },
        },
    }
    saved_items = []
    runner = MacroRunner(
        MagicMock(),
        MagicMock(),
        MagicMock(),
        get_auto_shop_settings=lambda: settings,
        save_auto_shop_item_state=lambda shop, key, state: saved_items.append(
            (shop, key, state)
        ),
    )
    cancel = {"x": 579, "y": 420, "w": 181, "h": 28}
    runner._shop_read_observation = MagicMock(
        side_effect=AssertionError("The public Auto Shop path must not use OCR")
    )
    monkeypatch.setattr("core.runner_shop.wm.show_window", lambda _hwnd: None)
    monkeypatch.setattr("core.runner_shop.wm.activate_window", lambda _hwnd: True)
    monkeypatch.setattr(runner, "_ensure_lobby", lambda *_args: True)
    monkeypatch.setattr(runner, "_shop_enter_gold_shop", lambda *_args: True)
    monkeypatch.setattr(
        runner,
        "_shop_find_visible_item",
        lambda *_args: {"x": 429, "y": 325, "w": 61, "h": 55},
    )
    monkeypatch.setattr(runner, "_shop_find_terminal_label", lambda *_args: None)
    monkeypatch.setattr(runner, "_shop_open_purchase_modal", lambda *_args: cancel)
    monkeypatch.setattr(runner, "_shop_configure_amount", lambda *_args: True)
    monkeypatch.setattr(runner, "_shop_confirm_purchase", lambda *_args: True)
    monkeypatch.setattr("core.runner_shop.vision.find_image", lambda *_args, **_kwargs: None)
    monkeypatch.setattr("core.runner_shop.vision.ref_to_screen", lambda _hwnd, x, y: (x, y))
    monkeypatch.setattr("core.runner_shop.time.sleep", lambda _seconds: None)

    runner._run_auto_shop(1, threading.Event())

    runner._shop_read_observation.assert_not_called()
    assert saved_items[-1][2]["status"] == auto_shop.STATUS_PENDING


def test_open_modal_clicks_the_green_buy_region_without_matching_a_price(monkeypatch):
    """Price artwork must not decide whether a known card Buy can be clicked."""
    runner = _runner([])
    item_match = {"x": 429, "y": 245, "w": 61, "h": 55}
    cancel = {"x": 579, "y": 420, "w": 181, "h": 28}
    clicked = []
    monkeypatch.setattr(
        "core.runner_shop.vision.capture_game_bgr",
        lambda *_args, **_kwargs: np.full((43, 142, 3), (0, 255, 70), dtype=np.uint8),
    )
    monkeypatch.setattr(
        "core.runner_shop.vision.find_color_run",
        lambda *_args, **_kwargs: pytest.fail("Text must not break a total-color check"),
    )
    monkeypatch.setattr(
        "core.runner_shop.vision.wait_for_image",
        lambda _hwnd, name, **_kwargs: cancel if name == "shop_cancel" else pytest.fail(
            "A dynamic Buy price must not be searched"
        ),
    )
    monkeypatch.setattr(
        "core.runner_shop.vision.click_match",
        lambda _mouse, _hwnd, match: clicked.append(match),
    )

    assert runner._shop_open_purchase_modal(1, item_match, threading.Event()) == cancel
    assert clicked == [
        {"x": 391, "y": 382, "w": 140, "h": 42, "cx": 461, "cy": 403},
    ]


def test_max_amount_clicks_the_modal_toggle_without_searching_max_or_min(monkeypatch):
    """The stable Cancel anchor makes a second template search unnecessary."""
    runner = _runner([])
    cancel = {"x": 579, "y": 420, "w": 181, "h": 28}
    monkeypatch.setattr(
        "core.runner_shop.vision.find_image",
        lambda *_args, **_kwargs: pytest.fail("Max and Min templates must not be searched"),
    )
    monkeypatch.setattr(
        "core.runner_shop.vision.ref_to_screen",
        lambda _hwnd, x, y: (x, y),
    )

    assert runner._shop_configure_amount(1, cancel, "max", 50, threading.Event()) is True
    runner._mouse.click.assert_called_once_with(734, 388)
