from telegram import Update
from telegram.ext import CallbackContext

from poetrybot.database import store
from poetrybot.database.api import get_a_random_poem


def quote(update: Update, context: CallbackContext) -> None:
    """Get a poem."""
    with store.get_session() as s:
        poem = get_a_random_poem(s)

    update.message.reply_text(poem.verses)
