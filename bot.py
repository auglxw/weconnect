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
from dbfunctions import get_user

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("%s started the bot", update.effective_chat.id)
    await update.message.reply_text("Hello", reply_markup=main_menu_keyboard())
    

def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Register/ Edit', callback_data='register')],
                [InlineKeyboardButton('Find Match', callback_data='findmatch')]]
    return InlineKeyboardMarkup(keyboard)

async def sendMsg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_profile = get_user(update.effective_user.id)
    logger.info("%s sent %s", update.effective_chat.id, update.message.text)
    await context.bot.send_message(user_profile["room_id"], update.message.text)

async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Thanks for chatting!")

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Need some help?\n/register to create your profile\n/find to find a match\n/help if you need my help again")


def main() -> None:
    application = Application.builder().token("5474527930:AAFAFk88EYYIfAi9YQkgvdZe_5wqg-WBAFU").build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("find", find_match_handler))
    application.add_handler(CommandHandler("exit", exit))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, sendMsg))
    application.add_handler(PollAnswerHandler(receive_poll_answer))
    application.add_handler(CallbackQueryHandler(register, "register"))
    application.add_handler(CallbackQueryHandler(find_match_handler, "findmatch"))
    # application.add_handler(CallbackQueryHandler(print("join"), "join"))

    application.add_handler(CommandHandler("findmatch", find_match_handler))
    application.add_handler(CommandHandler("stopsearch", exit_search_handler))
    
    application.run_webhook(listen="0.0.0.0",
                      port=int(os.environ.get('PORT', 5000)),
                      url_path="5474527930:AAFAFk88EYYIfAi9YQkgvdZe_5wqg-WBAFU",
                      webhook_url=  "https://lifehack22.herokuapp.com/5474527930:AAFAFk88EYYIfAi9YQkgvdZe_5wqg-WBAFU"
                      )
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
