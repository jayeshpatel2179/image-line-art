import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

def _rotated(size: str) -> str:
    """Swaps WxH -> HxW so the vertical default matches the same pixel budget as
    whatever horizontal size is configured (e.g. "1824x1024" -> "1024x1824")."""
    if "x" in size:
        w, _, h = size.partition("x")
        if w.isdigit() and h.isdigit():
            return f"{h}x{w}"
    return "1024x1536"


TEXT_MODEL = os.getenv("TEXT_MODEL", "gpt-4o")
IMAGE_MODEL = os.getenv("IMAGE_MODEL", "gpt-image-2")
IMAGE_SIZE_HORIZONTAL = os.getenv("IMAGE_SIZE_HORIZONTAL", os.getenv("IMAGE_SIZE", "1824x1024"))
IMAGE_SIZE_VERTICAL = os.getenv("IMAGE_SIZE_VERTICAL", _rotated(IMAGE_SIZE_HORIZONTAL))
IMAGE_QUALITY = os.getenv("IMAGE_QUALITY", "high")

STYLE_REFERENCE_ENABLED = os.getenv("STYLE_REFERENCE_ENABLED", "true").lower() == "true"
STYLE_REFERENCE_COUNT = int(os.getenv("STYLE_REFERENCE_COUNT", "2"))
STYLE_REFERENCE_DIR = BASE_DIR / os.getenv("STYLE_REFERENCE_DIR", "images-sample")

GENERATION_RETENTION_SECONDS = int(os.getenv("GENERATION_RETENTION_SECONDS", "300"))

MASTER_PROMPT_PATH = BASE_DIR / "config" / "master_prompt.txt"
GENERATIONS_DIR = BASE_DIR / "storage" / "generations"

MASTER_PROMPT = MASTER_PROMPT_PATH.read_text(encoding="utf-8")
