import logging

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from poetrybot.database import store
from poetrybot.database.api import get_a_random_poem, is_user_in_accept_list

logger = logging.getLogger(__name__)


def quote(update: Update, context: CallbackContext) -> None:
    """Get a poem."""
    with store.get_session() as s:

        user_id = update.effective_user.id
        username = update.effective_user.username
        if not is_user_in_accept_list(s, user_id=update.effective_user.id):
            logger.warning(
                "Telegram user with id '{}' and username"
                " '{}' tried to get a quote.".format(user_id, username)
            )
            return

        poem = get_a_random_poem(s)

        reply = f"{poem.verses}\n\n_{poem.author.name}_" if poem else "No quote found!"

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=reply, parse_mode=ParseMode.MARKDOWN
    )
