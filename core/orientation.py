"""Fixed frame-shape clauses and image sizes for the user's orientation choice."""

from config import settings

ORIENTATION_LABELS = {
    "horizontal": "Horizontal (16:9)",
    "vertical": "Vertical (9:16)",
}

_ORIENTATION_CLAUSES = {
    "horizontal": "The overall canvas is a wide 16:9 landscape frame.",
    "vertical": "The overall canvas is a tall 9:16 portrait frame.",
}

_ORIENTATION_SIZES = {
    "horizontal": settings.IMAGE_SIZE_HORIZONTAL,
    "vertical": settings.IMAGE_SIZE_VERTICAL,
}


def apply_orientation(prompt: str, orientation: str) -> str:
    return f"{prompt} {_ORIENTATION_CLAUSES[orientation]}"


def get_image_size(orientation: str) -> str:
    return _ORIENTATION_SIZES[orientation]
