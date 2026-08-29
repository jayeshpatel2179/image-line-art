"""Adds the house-style headline text on top of an already-generated (text-free) image."""

from pathlib import Path

from openai import AsyncOpenAI

from config import settings
from core.image_renderer import _decode_and_save

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


def _build_text_prompt(raw_text: str) -> str:
    return (
        "Add bold, condensed, ALL-CAPS sans-serif headline text directly onto this image. "
        "Do not change the illustration, character, props, composition, or background in any "
        "way — only add the text into the existing empty negative-space area. "
        "Split the following text naturally across 2-4 lines as needed for readability; do not "
        "reword, paraphrase, add, or remove a single word — render it exactly as given, only "
        f"choosing where to break lines: \"{raw_text.strip()}\". "
        "All lines except the last are dark charcoal ink, matching the illustration's line color. "
        "The final line is vivid blue (#2E7DE1). The rendered words must exactly match the given "
        "text, word for word."
    )


async def add_text_overlay(base_image_path: Path, raw_text: str, size: str) -> tuple[bytes, Path]:
    prompt = _build_text_prompt(raw_text)

    with open(base_image_path, "rb") as f:
        response = await client.images.edit(
            model=settings.IMAGE_MODEL,
            image=[f],
            prompt=prompt,
            size=size,
            quality=settings.IMAGE_QUALITY,
        )

    return _decode_and_save(response)
