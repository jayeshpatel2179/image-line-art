"""Stage B: renders the final prompt into an image with gpt-image-2."""

import asyncio
import base64
import time
import uuid
from contextlib import ExitStack
from pathlib import Path

from openai import AsyncOpenAI

from config import settings
from core.style_reference import pick_reference_images

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

# Keeps references to the scheduled-delete tasks so they aren't garbage-collected
# mid-sleep (asyncio only holds a weak reference to a task once nothing else does).
_pending_deletes: set[asyncio.Task] = set()


async def generate_image(prompt: str) -> tuple[bytes, Path]:
    reference_paths = pick_reference_images()

    if reference_paths:
        with ExitStack() as stack:
            files = [stack.enter_context(open(p, "rb")) for p in reference_paths]
            try:
                response = await client.images.edit(
                    model=settings.IMAGE_MODEL,
                    image=files,
                    prompt=prompt,
                    size=settings.IMAGE_SIZE,
                    quality=settings.IMAGE_QUALITY,
                )
                return _decode_and_save(response)
            except Exception:
                # Reference-grounded edit call failed (e.g. size/param mismatch on the
                # edit endpoint) — fall back to a plain text-to-image call below.
                pass

    response = await client.images.generate(
        model=settings.IMAGE_MODEL,
        prompt=prompt,
        size=settings.IMAGE_SIZE,
        quality=settings.IMAGE_QUALITY,
    )
    return _decode_and_save(response)


def _decode_and_save(response) -> tuple[bytes, Path]:
    image_bytes = base64.b64decode(response.data[0].b64_json)

    settings.GENERATIONS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = settings.GENERATIONS_DIR / f"{int(time.time())}_{uuid.uuid4().hex[:8]}.png"
    out_path.write_bytes(image_bytes)
    _schedule_delete(out_path, settings.GENERATION_RETENTION_SECONDS)

    return image_bytes, out_path


def _schedule_delete(path: Path, delay_seconds: int) -> None:
    async def _delete_after_delay() -> None:
        await asyncio.sleep(delay_seconds)
        path.unlink(missing_ok=True)

    task = asyncio.create_task(_delete_after_delay())
    _pending_deletes.add(task)
    task.add_done_callback(_pending_deletes.discard)
