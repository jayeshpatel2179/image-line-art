"""Fixed composition clauses appended to the scene prompt based on the user's placement choice."""

PLACEMENT_LABELS = {
    "left": "Left",
    "right": "Right",
    "center": "Center",
    "bottom": "Bottom",
}

_PLACEMENT_CLAUSES = {
    "left": (
        "The character and all supporting props are positioned on the LEFT side of the frame, "
        "occupying roughly 40-55% of the width, with generous empty flat cream-colored negative "
        "space filling the right side."
    ),
    "right": (
        "The character and all supporting props are positioned on the RIGHT side of the frame, "
        "occupying roughly 40-55% of the width, with generous empty flat cream-colored negative "
        "space filling the left side."
    ),
    "center": (
        "The character and all supporting props are centered in the frame, with balanced empty "
        "flat cream-colored negative space distributed evenly on the left and right sides."
    ),
    "bottom": (
        "The character and all supporting props are positioned along the BOTTOM of the frame, "
        "with generous empty flat cream-colored negative space filling the upper portion."
    ),
}


def apply_placement(scene_prompt: str, placement: str) -> str:
    return f"{scene_prompt} {_PLACEMENT_CLAUSES[placement]}"
