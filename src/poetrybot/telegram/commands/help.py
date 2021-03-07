from telegram import Update
from telegram.ext import CallbackContext


def help(update: Update, context: CallbackContext) -> None:
    """Give help to users."""
    update.message.reply_text("Hello! Use /quote to get a random poem!")
