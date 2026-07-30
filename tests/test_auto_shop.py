from datetime import datetime, timezone

import cv2
import numpy as np
import pytest

from core import auto_shop
from core import vision


UTC = timezone.utc


def _epoch(year, month, day, hour=0, minute=0, second=0):
    return datetime(year, month, day, hour, minute, second, tzinfo=UTC).timestamp()


def test_auto_shop_catalog_has_every_gold_shop_item_and_asset():
    expected = [
        ("cursed_boba", "Cursed Boba", 50),
        ("red_flower", "Red Flower", 75),
        ("frown_fruit", "Frown Fruit", 100),
        ("delicious_pie", "Delicious Pie", 125),
        ("mana_flask", "Mana Flask", 150),
        ("trait_crystal", "Trait Crystal", 25),
        ("sprite_grey", "Sprite (Grey)", 25),
        ("equipment_reroll", "Equipment Reroll", 10),
        ("equipment_lock", "Equipment Lock", 10),
        ("stat_reroll", "Stat Reroll", 10),
        ("stat_lock", "Stat Lock", 10),
    ]

    assert [(item["key"], item["name"], item["stock"]) for item in auto_shop.AUTO_SHOP_ITEMS] == expected
    for item in auto_shop.AUTO_SHOP_ITEMS:
        assert vision.template_variant_paths(item["template"])
    for template in auto_shop.AUTO_SHOP_UI_TEMPLATES.values():
        assert vision.template_variant_paths(template)


def test_auto_shop_uses_the_same_utc_midnight_reset_as_challenge():
    import main

    assert auto_shop.AUTO_SHOP_RESET_SCHEDULE == main.CHALLENGE_RESET_SCHEDULE
    assert auto_shop.current_auto_shop_period(_epoch(2026, 7, 29, 23, 59, 59)) == "2026-07-29"
    assert auto_shop.current_auto_shop_period(_epoch(2026, 7, 30, 0, 0, 0)) == "2026-07-30"


def test_purchase_plan_counts_manual_purchases_toward_numeric_target():
    plan = auto_shop.calculate_purchase_plan("cursed_boba", 15, current_left=40)

    assert plan == {
        "daily_maximum": 50,
        "current_left": 40,
        "already_bought": 10,
        "desired_total": 15,
        "pending_amount": 5,
        "status": auto_shop.STATUS_PENDING,
    }


def test_purchase_plan_buys_only_the_difference_after_target_increase():
    plan = auto_shop.calculate_purchase_plan("cursed_boba", 20, current_left=35)

    assert plan["already_bought"] == 15
    assert plan["pending_amount"] == 5


def test_purchase_plan_stops_when_reduced_target_was_already_met():
    plan = auto_shop.calculate_purchase_plan("cursed_boba", 5, current_left=40)

    assert plan["pending_amount"] == 0
    assert plan["status"] == auto_shop.STATUS_COMPLETED


def test_max_target_uses_every_remaining_item():
    plan = auto_shop.calculate_purchase_plan("trait_crystal", "Max", current_left=17)

    assert plan["desired_total"] == 25
    assert plan["pending_amount"] == 17


def test_zero_stock_is_terminal_out_of_stock():
    plan = auto_shop.calculate_purchase_plan("equipment_lock", "max", current_left=0)

    assert plan["pending_amount"] == 0
    assert plan["status"] == auto_shop.STATUS_OUT_OF_STOCK


@pytest.mark.parametrize("target", [0, 51, True, "invalid", None])
def test_invalid_targets_are_rejected(target):
    with pytest.raises(ValueError):
        auto_shop.calculate_purchase_plan("cursed_boba", target, current_left=50)


def test_left_ocr_requires_two_matching_in_range_reads():
    assert auto_shop.parse_left_count("50 Left!", 50) == 50
    assert auto_shop.parse_left_count("150 Left!", 50) is None
    assert auto_shop.consensus_left_count([50, 50, 5], 50) == 50
    assert auto_shop.consensus_left_count([50, 49, None], 50) is None


def test_visual_signature_detects_a_small_text_change():
    before = np.zeros((24, 96, 3), dtype=np.uint8)
    after = before.copy()
    cv2.putText(before, "50 Left!", (2, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
    cv2.putText(after, "49 Left!", (2, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

    before_signature = auto_shop.build_stock_signature(before)
    after_signature = auto_shop.build_stock_signature(after)

    assert auto_shop.stock_signature_distance(before_signature, after_signature) > 0
    assert auto_shop.stock_signature_distance(before_signature, before_signature) == 0


def test_stock_verification_requires_ocr_and_visual_change_to_agree():
    assert (
        auto_shop.classify_stock_verification(50, 49, True)
        == auto_shop.VERIFICATION_PROGRESS
    )
    assert (
        auto_shop.classify_stock_verification(50, 50, False)
        == auto_shop.VERIFICATION_UNCHANGED
    )
    assert (
        auto_shop.classify_stock_verification(50, 49, False)
        == auto_shop.VERIFICATION_PENDING
    )
    assert (
        auto_shop.classify_stock_verification(50, None, True)
        == auto_shop.VERIFICATION_PENDING
    )
    assert (
        auto_shop.classify_stock_verification(50, None, None, out_of_stock=True)
        == auto_shop.VERIFICATION_OUT_OF_STOCK
    )


def test_min_means_max_is_already_selected():
    assert auto_shop.max_toggle_action(max_visible=True, min_visible=False) == auto_shop.MAX_TOGGLE_CLICK
    assert (
        auto_shop.max_toggle_action(max_visible=False, min_visible=True)
        == auto_shop.MAX_TOGGLE_ALREADY_SELECTED
    )
    assert auto_shop.max_toggle_action(max_visible=False, min_visible=False) == auto_shop.MAX_TOGGLE_UNKNOWN


def test_item_stops_after_three_failures_and_resets_next_period():
    state = auto_shop.fresh_item_state("2026-07-30")
    state = auto_shop.record_item_failure(state, "2026-07-30")
    state = auto_shop.record_item_failure(state, "2026-07-30")
    state = auto_shop.record_item_failure(state, "2026-07-30")

    assert state["attempts"] == 3
    assert state["status"] == auto_shop.STATUS_FAILED_TODAY

    reset = auto_shop.normalize_item_state(state, "2026-07-31")
    assert reset == auto_shop.fresh_item_state("2026-07-31")


def test_navigation_failures_have_a_separate_daily_limit():
    state = auto_shop.fresh_shop_state("2026-07-30")
    state = auto_shop.record_navigation_failure(state, "2026-07-30")
    state = auto_shop.record_navigation_failure(state, "2026-07-30")
    state = auto_shop.record_navigation_failure(state, "2026-07-30")

    assert state["navigation_failures"] == 3
    assert state["status"] == auto_shop.STATUS_FAILED_TODAY
    assert auto_shop.normalize_shop_state(state, "2026-07-31") == auto_shop.fresh_shop_state("2026-07-31")


def test_cancel_click_is_near_the_far_right_edge_and_inside_the_button():
    point = auto_shop.cancel_right_edge_point(left=10, top=20, width=181, height=28)

    assert point == (185, 34)
    assert 10 <= point[0] < 191
    assert 20 <= point[1] < 48
