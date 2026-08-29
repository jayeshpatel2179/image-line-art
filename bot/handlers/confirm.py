import io

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import session_store
from core.image_renderer import generate_image
from core.orientation import apply_orientation, get_image_size
from core.placement import apply_placement
from core.text_overlay import add_text_overlay

ORIENTATION_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🖼️ Horizontal (16:9)", callback_data="orient:horizontal"),
            InlineKeyboardButton("📱 Vertical (9:16)", callback_data="orient:vertical"),
        ]
    ]
)

REVIEW_KEYBOARD_NO_TEXT = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("📝 Add Text", callback_data="add_text"),
            InlineKeyboardButton("🔄 Regenerate", callback_data="regenerate"),
            InlineKeyboardButton("✅ Done", callback_data="done"),
        ]
    ]
)

REVIEW_KEYBOARD_WITH_TEXT = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🔄 Regenerate", callback_data="regenerate"),
            InlineKeyboardButton("✅ Done", callback_data="done"),
        ]
    ]
)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id
    await query.answer()

    session = session_store.get_session(chat_id)
    if session is None:
        await context.bot.send_message(chat_id, "This session has expired — send a new line of text.")
        return

    data = query.data

    if data.startswith("place:"):
        session_store.set_placement(chat_id, data.split(":", 1)[1])
        await query.edit_message_text(
            "Horizontal or vertical image?",
            reply_markup=ORIENTATION_KEYBOARD,
        )
        return

    if data.startswith("orient:"):
        session_store.set_orientation(chat_id, data.split(":", 1)[1])
        await _generate_base_image(query, context, chat_id, session)
        return

    if data == "add_text":
        await _add_text(query, context, chat_id, session)
        return

    if data == "regenerate":
        if session.get("placement") is None or session.get("orientation") is None:
            await query.edit_message_caption(caption="Nothing to regenerate yet.")
            return
        await _generate_base_image(query, context, chat_id, session)
        return

    if data == "done":
        session_store.clear_session(chat_id)
        await query.edit_message_caption(caption="✅ Done! Send another line whenever you're ready.")
        return


async def _generate_base_image(query, context, chat_id, session) -> None:
    placement = session["placement"]
    orientation = session["orientation"]

    final_prompt = apply_orientation(apply_placement(session["scene_prompt"], placement), orientation)
    size = get_image_size(orientation)

    status_text = f"🎨 Generating the image ({placement}, {orientation})..."
    if query.message.photo:
        await query.edit_message_caption(caption=status_text)
    else:
        await query.edit_message_text(status_text)

    try:
        image_bytes, image_path = await generate_image(final_prompt, size)
    except Exception as exc:  # noqa: BLE001
        await context.bot.send_message(chat_id, f"Generation failed: {exc}")
        return

    session_store.set_current_image(chat_id, image_path)
    session_store.set_has_text(chat_id, False)

    await context.bot.send_photo(
        chat_id,
        photo=io.BytesIO(image_bytes),
        caption="No text yet. Add text, regenerate, or finish.",
        reply_markup=REVIEW_KEYBOARD_NO_TEXT,
    )


async def _add_text(query, context, chat_id, session) -> None:
    image_path = session.get("image_path")
    if image_path is None or not image_path.exists():
        await query.edit_message_caption(
            caption="That image is no longer available — send a new line of text."
        )
        return

    await query.edit_message_caption(caption="📝 Adding text...")

    try:
        image_bytes, new_image_path = await add_text_overlay(image_path, session["raw_text"])
    except Exception as exc:  # noqa: BLE001
        await context.bot.send_message(chat_id, f"Adding text failed: {exc}")
        return

    session_store.set_current_image(chat_id, new_image_path)
    session_store.set_has_text(chat_id, True)

    await context.bot.send_photo(
        chat_id,
        photo=io.BytesIO(image_bytes),
        caption="Text added. Regenerate or finish.",
        reply_markup=REVIEW_KEYBOARD_WITH_TEXT,
    )
