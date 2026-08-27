import io

from telegram import Update
from telegram.ext import ContextTypes

from bot import session_store
from core.image_renderer import generate_image


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id
    await query.answer()

    session = session_store.get_session(chat_id)
    if session is None:
        await query.edit_message_text("This prompt has expired — send a new line of text.")
        return

    if query.data == "cancel":
        session_store.clear_session(chat_id)
        await query.edit_message_text("Cancelled. Send another line whenever you're ready.")
        return

    if query.data == "edit":
        await query.edit_message_text(
            "Send the revised line (or a note on what to change) and I'll rebuild the prompt."
        )
        return

    if query.data == "generate":
        await query.edit_message_text("🎨 Generating the image...")
        try:
            image_bytes = await generate_image(session["final_prompt"])
        except Exception as exc:  # noqa: BLE001
            await context.bot.send_message(chat_id, f"Generation failed: {exc}")
            return

        await context.bot.send_photo(chat_id, photo=io.BytesIO(image_bytes))
        session_store.clear_session(chat_id)
