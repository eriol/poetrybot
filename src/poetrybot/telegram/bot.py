from telegram.ext import Application, CommandHandler

from .commands.help import help
from .commands.quote import quote


def run(config) -> None:
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("quote", quote))

    application.run_polling()
