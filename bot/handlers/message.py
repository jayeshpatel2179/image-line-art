from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import session_store
from core.prompt_architect import build_scene_prompt

PLACEMENT_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("⬅️ Left", callback_data="place:left"),
            InlineKeyboardButton("➡️ Right", callback_data="place:right"),
        ],
        [
            InlineKeyboardButton("⏺️ Center", callback_data="place:center"),
            InlineKeyboardButton("⬇️ Bottom", callback_data="place:bottom"),
        ],
    ]
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Send me one line of text and I'll turn it into a house-style illustration.\n\n"
        "First you'll pick where the illustration sits in the frame. I'll generate the image "
        "with no text yet — after that you can add the headline text, regenerate, or finish."
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_text = update.message.text.strip()

    if not user_text:
        return

    thinking = await update.message.reply_text("✍️ Writing the scene prompt...")

    try:
        scene_prompt = await build_scene_prompt(user_text)
    except Exception as exc:  # noqa: BLE001
        await thinking.edit_text(f"Couldn't build a prompt: {exc}")
        return

    session_store.set_scene_prompt(chat_id, user_text, scene_prompt)

    await thinking.edit_text(
        f"Here's the scene 👇\n\n{scene_prompt}\n\nWhere should the illustration sit?",
        reply_markup=PLACEMENT_KEYBOARD,
    )
