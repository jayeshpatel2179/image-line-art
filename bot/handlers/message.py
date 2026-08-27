from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import session_store
from core.prompt_architect import build_final_prompt

CONFIRM_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("✅ Generate", callback_data="generate"),
            InlineKeyboardButton("✏️ Edit", callback_data="edit"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel"),
        ]
    ]
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Send me one line of text and I'll turn it into a house-style visual.\n\n"
        "I'll show you the exact prompt before generating anything — you'll get "
        "Generate / Edit / Cancel buttons to confirm."
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_text = update.message.text.strip()

    if not user_text:
        return

    thinking = await update.message.reply_text("✍️ Writing the prompt...")

    try:
        final_prompt = await build_final_prompt(user_text)
    except Exception as exc:  # noqa: BLE001
        await thinking.edit_text(f"Couldn't build a prompt: {exc}")
        return

    session_store.set_pending_prompt(chat_id, user_text, final_prompt)

    await thinking.edit_text(
        f"Here's what I'll generate 👇\n\n{final_prompt}",
        reply_markup=CONFIRM_KEYBOARD,
    )
