from telegram.ext import Updater, CommandHandler

from .commands.help import help


def run(config) -> None:
    updater = Updater(config.TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("help", help))

    updater.start_polling()
    updater.idle()
