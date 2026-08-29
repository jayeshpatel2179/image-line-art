# image-art bot

Telegram bot: send one line of text → it's expanded into a text-free house-style scene prompt
(Stage A, `gpt-4o`) → you pick where the illustration sits (Left/Right/Center/Bottom) → you pick
Horizontal or Vertical → it's rendered with no text (Stage B, `gpt-image-2`) → you can then add
the headline text, regenerate the whole image, or finish.

## Setup

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Fill in `.env`:
- `TELEGRAM_BOT_TOKEN` — from [@BotFather](https://t.me/BotFather)
- `OPENAI_API_KEY` — needs access to both the text model and `gpt-image-2`

## Run

```
python -m bot.main
```

## How it works

1. You send a one-liner in Telegram.
2. The bot sends it, together with `config/master_prompt.txt`, to `TEXT_MODEL` — this returns
   one **text-free** scene prompt (house style + a scene matching the text's meaning and
   emotional tone). No headline text is generated at this stage.
3. The bot shows you that scene prompt with **Left / Right / Center / Bottom** buttons —
   pick where the illustration should sit in the frame.
4. The bot then asks **Horizontal (16:9) or Vertical (9:16)** — the shape of the canvas.
5. The bot appends the placement clause (`core/placement.py`) and the orientation clause
   (`core/orientation.py`) to the prompt, then calls `gpt-image-2` at the matching image size
   (`IMAGE_SIZE_HORIZONTAL` / `IMAGE_SIZE_VERTICAL`), grounded on 1–2 random images from
   `images-sample/` for style consistency when `STYLE_REFERENCE_ENABLED=true`. The image comes
   back with **no text on it**, along with **Add Text / Regenerate / Done** buttons.
6. From there:
   - **Add Text** — runs an `images.edit` call on that exact saved image, adding only the
     house-style headline (your original line, verbatim, split across 2-4 lines as needed —
     see `core/text_overlay.py`) without touching the illustration itself.
   - **Regenerate** — throws away the current image and renders a brand-new version from the
     same scene prompt + placement + orientation (no text), returning to the Add Text/Regenerate/Done
     screen.
   - **Done** — ends the session; whatever image is currently shown is the final result.

## Notes

- Session state (scene prompt, placement, orientation, current image path, per chat) is in-memory —
  restarting the bot clears any in-progress session. Fine for single-instance use; swap
  `bot/session_store.py` for Redis if you ever run more than one process.
- Every generated/edited image is saved to `storage/generations/`, then auto-deleted from
  disk `GENERATION_RETENTION_SECONDS` after creation (default 300s / 5 min). This only
  clears the local disk copy — it doesn't unsend the photo from the Telegram chat. If you
  tap **Add Text** more than 5 minutes after the base image was generated, the base file
  will already be gone and you'll be asked to start over.
- To change the visual style itself, edit `config/master_prompt.txt` — nothing else needs
  to change.

# image-line-art
