from telegram import Update
from telegram.ext import CallbackContext

from poetrybot.database import store
from poetrybot.database.api import get_a_random_poem


def quote(update: Update, context: CallbackContext) -> None:
    """Get a poem."""
    s = store.session()
    poem = get_a_random_poem(s)
    store.session.remove()

    update.message.reply_text(poem.verses)
