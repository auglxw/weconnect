from telegram import (
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

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    questions_interest = ["Race", "Sexual Orientation", "Occupation", "Education", "Physical Capabilities"]
    questions_shared = ["Race", "Sexual Orientation", "Occupation", "Education", "Physical Capabilities", "None"]
    message = await context.bot.send_poll(
        update.effective_chat.id,
        "Select the following communities you are interested in.",
        questions_interest,
        is_anonymous=False,
        allows_multiple_answers=True,
    )
    payload = {
        message.poll.id: {
            "questions": questions_interest,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
        }
    }
    context.bot_data.update(payload)
    
    message = await context.bot.send_poll(
        update.effective_chat.id,
        "Select the following communities you identify with.",
        questions_shared,
        is_anonymous=False,
        allows_multiple_answers=True,
    )
    payload = {
        message.poll.id: {
            "questions": questions_shared,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
        }
    }
    context.bot_data.update(payload)


async def receive_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    answer = update.poll_answer
    answered_poll = context.bot_data[answer.poll_id]
    try:
        questions = answered_poll["questions"]
    except KeyError:
        return
    
    # Upload selected options to database here
    selected_options = answer.option_ids
    answer_string = ""
    for question_id in selected_options:
        if question_id != selected_options[-1]:
            answer_string += questions[question_id] + "\n"
        else:
            answer_string += questions[question_id]
    await context.bot.stop_poll(answered_poll["chat_id"], answered_poll["message_id"])
    await context.bot.delete_message(answered_poll["chat_id"], answered_poll["message_id"])
    await context.bot.send_message(
        answered_poll["chat_id"],
        f"You are interested in learning more about:\n{answer_string}",
        parse_mode=ParseMode.HTML,
    )


async def receive_poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """On receiving polls, reply to it by a closed poll copying the received poll"""
    actual_poll = update.effective_message.poll
    # Only need to set the question and options, since all other parameters don't matter for
    # a closed poll
    await update.effective_message.reply_poll(
        question=actual_poll.question,
        options=[o.text for o in actual_poll.options],
        # with is_closed true, the poll/quiz is immediately closed
        is_closed=True,
        reply_markup=ReplyKeyboardRemove(),
    )
