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

from dbfunctions import (insert_user, can_edit_user, edit_user)

from matchfunctions import find_match


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("chat id: ", update.effective_chat.id)
    print("user id: ", update.effective_user.id)
    questions_interest = ["Race", "Sexual Orientation",
                          "Occupation", "Education", "Physical Capabilities"]
    questions_share = ["Race", "Sexual Orientation",
                       "Occupation", "Education", "Physical Capabilities", "None"]
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
            "type": "interest",
        }
    }
    context.bot_data.update(payload)

    message = await context.bot.send_poll(
        update.effective_chat.id,
        "Select the following communities you identify with.",
        questions_share,
        is_anonymous=False,
        allows_multiple_answers=True,
    )
    payload = {
        message.poll.id: {
            "questions": questions_share,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
            "type": "share",
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
    user_id = update.effective_user.id

    # If interest:

    if answered_poll["type"] == "share" and 5 in selected_options:
        answer_string = "That's alright! We are all here to learn :)"
    else:
        if answered_poll["type"] == "share":
            print("inputting user: share")
            if can_edit_user(user_id):
                edit_user("share", selected_options, user_id)
            else:
                insert_user("share", selected_options,
                            user_id)
            answer_string = "You are open to sharing about:\n"
        elif answered_poll["type"] == "interest":
            print("inputting user: interest")
            if can_edit_user(user_id):
                edit_user("interest", selected_options,
                          user_id)
            else:
                insert_user("interest", selected_options,
                            user_id)
            answer_string = "You are interested in learning more about:\n"
        for question_id in selected_options:
            if question_id != selected_options[-1]:
                answer_string += questions[question_id] + "\n"
            else:
                answer_string += questions[question_id]
    await context.bot.stop_poll(answered_poll["chat_id"], answered_poll["message_id"])
    await context.bot.delete_message(answered_poll["chat_id"], answered_poll["message_id"])
    await context.bot.send_message(
        answered_poll["chat_id"],
        answer_string,
        parse_mode=ParseMode.HTML,
    )
