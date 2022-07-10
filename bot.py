import logging
import os
from telegram import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    MenuButtonDefault,
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
)
from matchfunctions import (find_match_handler, exit_search_handler)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("%s started the bot", update.effective_chat.id)
    await update.message.reply_text("Hello", reply_markup=main_menu_keyboard())
    

def main_menu_keyboard():
    # keyboard = [[InlineKeyboardButton('Register/ Edit', callback_data='register')],
    #             [InlineKeyboardButton('Find', callback_data='find'),
    #             InlineKeyboardButton('Join', callback_data='join')]]

    keyboard = [[InlineKeyboardButton('Register/ Edit', callback_data='register')],
                [InlineKeyboardButton('Find Match', callback_data='findmatch')]]
    return InlineKeyboardMarkup(keyboard)

async def find(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(update.effective_chat.id, "You are now chatting.")
    # create the 'room' id aka save the chat id of the other user

async def sendMsg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # if there is a 'room' id
    # else do nothing
    logger.info("%s sent %s", update.effective_chat.id, update.message.text)
    await context.bot.send_message("428599836", update.message.text)

async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Thanks for chatting!")
    # clear 'room' id from database

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Need some help?\n/register to create your profile\n/edit to edit your profile\n/find to find a match\n/help if you need my help again")


def main() -> None:
    application = Application.builder().token("5474527930:AAFAFk88EYYIfAi9YQkgvdZe_5wqg-WBAFU").build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("edit", register))
    application.add_handler(CommandHandler("find", find))
    application.add_handler(CommandHandler("exit", exit))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, sendMsg))
    application.add_handler(PollAnswerHandler(receive_poll_answer))
    application.add_handler(CallbackQueryHandler(register, "register"))
    application.add_handler(CallbackQueryHandler(find, "find"))
    # application.add_handler(CallbackQueryHandler(print("join"), "join"))

    application.add_handler(CommandHandler("findmatch", find_match_handler))
    application.add_handler(CommandHandler("stopsearch", exit_search_handler))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
