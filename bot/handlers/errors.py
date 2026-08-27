import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def handle_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Unhandled error while processing update: %s", update, exc_info=context.error)

    if isinstance(update, Update) and update.effective_chat:
        await context.bot.send_message(
            update.effective_chat.id, "Something went wrong on my end — please try again."
        )
