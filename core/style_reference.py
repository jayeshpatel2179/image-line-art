"""Picks a small, stable set of sample images to ground gpt-image-2 on the house style."""

import random

from config import settings

_SUPPORTED_EXT = {".png", ".jpg", ".jpeg", ".webp"}


def pick_reference_images() -> list:
    if not settings.STYLE_REFERENCE_ENABLED:
        return []

    candidates = sorted(
        p for p in settings.STYLE_REFERENCE_DIR.iterdir() if p.suffix.lower() in _SUPPORTED_EXT
    )
    if not candidates:
        return []

    count = min(settings.STYLE_REFERENCE_COUNT, len(candidates))
    return random.sample(candidates, count)
