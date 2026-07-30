"""Offline-safe visual helpers for the Gold Shop item list.

All coordinates produced here stay in the same reference space as the item
match returned by :mod:`core.vision`. Re-finding the item after every scroll
therefore relocates the stock label without relying on page coordinates.
"""

from collections import Counter
from typing import Iterable, Mapping, Optional

import numpy as np

from . import auto_shop, ocr


STOCK_REGION_BASE_ICON_WIDTH = 60
STOCK_REGION_BASE_LEFT = -12
STOCK_REGION_BASE_TOP = -18
STOCK_REGION_BASE_WIDTH = 64
STOCK_REGION_BASE_HEIGHT = 18

_OCR_CONFIG = "--psm 7 -c tessedit_char_whitelist=0123456789"
_OCR_SHARPEN_AMOUNTS = (0.0, 1.5)


def stock_region_from_item_match(match: Mapping) -> tuple:
    """Derive the ``Left!`` crop from the freshly located item icon."""
    try:
        x = int(match["x"])
        y = int(match["y"])
        width = int(match["w"])
        height = int(match["h"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Item match must contain integer x, y, w, and h values") from exc
    if width <= 0 or height <= 0:
        raise ValueError("Item match dimensions must be positive")

    scale = width / STOCK_REGION_BASE_ICON_WIDTH
    region_x = x + round(STOCK_REGION_BASE_LEFT * scale)
    region_y = y + round(STOCK_REGION_BASE_TOP * scale)
    region_width = max(1, round(STOCK_REGION_BASE_WIDTH * scale))
    region_height = max(1, round(STOCK_REGION_BASE_HEIGHT * scale))
    return region_x, region_y, region_width, region_height


def crop_region(frame_bgr: np.ndarray, region: tuple) -> np.ndarray:
    """Crop a validated reference-space region from a captured frame."""
    if frame_bgr is None or frame_bgr.size == 0:
        raise ValueError("Frame cannot be empty")
    x, y, width, height = (int(value) for value in region)
    frame_height, frame_width = frame_bgr.shape[:2]
    if width <= 0 or height <= 0:
        raise ValueError("Crop dimensions must be positive")
    if x < 0 or y < 0 or x + width > frame_width or y + height > frame_height:
        raise ValueError("Stock region falls outside the captured frame")
    return frame_bgr[y:y + height, x:x + width].copy()


def _ocr_values(crop_bgr: np.ndarray, daily_maximum: int) -> list:
    try:
        engine = ocr.get_pytesseract()
    except ocr.TesseractNotAvailable:
        engine = None
    values = []
    for sharpen_amount in _OCR_SHARPEN_AMOUNTS:
        for mask in ocr.candidate_masks(crop_bgr, sharpen_amount=sharpen_amount):
            text = ocr.ocr_mask(engine, mask, _OCR_CONFIG)
            value = auto_shop.parse_left_count(text, daily_maximum)
            if value is not None:
                values.append(value)
    return values


def read_left_count(crop_bgr: np.ndarray, daily_maximum: int) -> Optional[int]:
    """Read one bounded stock count through a strict preprocessing vote."""
    values = _ocr_values(crop_bgr, daily_maximum)
    if not values:
        return None
    ranked = Counter(values).most_common()
    best_value, best_votes = ranked[0]
    second_votes = ranked[1][1] if len(ranked) > 1 else 0
    if best_votes < 2 or best_votes == second_votes:
        return None
    return best_value


def read_left_consensus(crops_bgr: Iterable[np.ndarray], daily_maximum: int) -> Optional[int]:
    """Read three short frames and require two identical stock values."""
    readings = [read_left_count(crop, daily_maximum) for crop in crops_bgr]
    return auto_shop.consensus_left_count(readings, daily_maximum)


def stock_visual_changed(first_signature: str, second_signature: str, threshold: float = 0.005) -> bool:
    """Return whether bright stock-label pixels changed beyond capture noise."""
    if threshold < 0 or threshold > 1:
        raise ValueError("Visual-change threshold must be between 0 and 1")
    return auto_shop.stock_signature_distance(first_signature, second_signature) > threshold
