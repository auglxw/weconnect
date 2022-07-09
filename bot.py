#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that works with polls. Only 3 people are allowed to interact with each
poll/quiz the bot generates. The preview command generates a closed poll/quiz, exactly like the
one the user sends the bot
"""
import logging

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    Poll,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    User,
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    PollAnswerHandler,
    PollHandler,
    filters,
)
from register import (
    register,
    receive_poll_answer,
    receive_poll,
)
from matchfunctions import find_match

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello", reply_markup=main_menu_keyboard()
                                    )


def main_menu_keyboard():
    # keyboard = [[InlineKeyboardButton('Register/ Edit', callback_data='register')],
    #             [InlineKeyboardButton('Find', callback_data='find'),
    #             InlineKeyboardButton('Join', callback_data='join')]]

    keyboard = [[InlineKeyboardButton('Register/ Edit', callback_data='register')],
                [InlineKeyboardButton('Find Match', callback_data='find_match')]]
    return InlineKeyboardMarkup(keyboard)


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display a help message"""
    await update.message.reply_text("Use /quiz, /poll or /preview to test this bot.")


def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(
        "5474527930:AAFAFk88EYYIfAi9YQkgvdZe_5wqg-WBAFU").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("edit", register))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(MessageHandler(filters.POLL, receive_poll))
    application.add_handler(PollAnswerHandler(receive_poll_answer))

    application.add_handler(CallbackQueryHandler(register, "register"))
    # application.add_handler(CallbackQueryHandler(print("find"), "find"))
    # application.add_handler(CallbackQueryHandler(print("join"), "join"))

    application.add_handler(CommandHandler("find_match", find_match))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
