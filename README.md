# image-art bot

Telegram bot: send one line of text → it's expanded into a full house-style image prompt
(Stage A, `gpt-4o`) → you confirm it with a button → it's rendered (Stage B, `gpt-image-2`) →
the image comes back in chat.

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
2. The bot sends it, together with `config/master_prompt.txt`, to `TEXT_MODEL` — this
   returns one finished image prompt (house style + a scene matching the text's meaning
   and emotional tone + the two-line headline text to render).
3. The bot shows you that exact prompt with **Generate / Edit / Cancel** buttons. Nothing
   is generated until you tap Generate.
4. **Generate** calls `gpt-image-2` (grounded on 1–2 random images from `images-sample/`
   for style consistency, when `STYLE_REFERENCE_ENABLED=true`) and sends back the image.
   **Edit** lets you send a revised line, which restarts at step 2. **Cancel** drops it.

## Notes

- Session state (the pending prompt per chat) is in-memory — restarting the bot clears
  any unconfirmed prompts. Fine for single-instance use; swap `bot/session_store.py` for
  Redis if you ever run more than one process.
- Every generated image is also saved to `storage/generations/`, then auto-deleted from
  disk `GENERATION_RETENTION_SECONDS` after creation (default 300s / 5 min). This only
  clears the local disk copy — it doesn't unsend the photo from the Telegram chat.
- To change the visual style itself, edit `config/master_prompt.txt` — nothing else needs
  to change.

# image-line-art
