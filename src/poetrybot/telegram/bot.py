from telegram.ext import CommandHandler, Updater

from .commands.help import help
from .commands.quote import quote


def run(config) -> None:
    updater = Updater(config.TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("quote", quote))

    updater.start_polling()
    updater.idle()
