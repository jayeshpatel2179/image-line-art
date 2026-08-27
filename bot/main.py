import logging

from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters

from bot.handlers import confirm, errors, message
from config import settings

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)


def main() -> None:
    app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", message.start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message.handle_text))
    app.add_handler(CallbackQueryHandler(confirm.handle_callback))
    app.add_error_handler(errors.handle_error)

    app.run_polling()


if __name__ == "__main__":
    main()
