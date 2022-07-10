import logging
import os
from telegram import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    Poll,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
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
from chat import SocketIO

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello", reply_markup=main_menu_keyboard())
    

def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Register/ Edit', callback_data='register')],
                [InlineKeyboardButton('Find', callback_data='find'),
                InlineKeyboardButton('Join', callback_data='join')]]
    return InlineKeyboardMarkup(keyboard)

async def find(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(update.effective_chat.id, "Joining a room!")
    await SocketIO.connect()
    await SocketIO.beginChat("123")

async def sendMsg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(update.message.text)
    await SocketIO.sendMessage(update.message.text, "123", update.effective_chat.id)

async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await SocketIO.disconnect()
    await update.message.reply_text("Thanks for chatting!")

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Use /quiz, /poll or /preview to test this bot.")


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

    application.run_polling()


if __name__ == "__main__":
    main()
