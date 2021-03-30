import logging

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from poetrybot.database import store
from poetrybot.database.api import get_a_random_poem

logger = logging.getLogger(__name__)


def quote(update: Update, context: CallbackContext) -> None:
    """Get a poem."""
    with store.get_session() as s:
        poem = get_a_random_poem(s)

        reply = f"{poem.verses}\n\n_{poem.author.name}_" if poem else "No quote found!"

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=reply, parse_mode=ParseMode.MARKDOWN
    )
