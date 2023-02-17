from telegram import Update
from telegram.ext import ContextTypes


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Give help to users."""
    await update.message.reply_text("Hello! Use /quote to get a random poem!")
