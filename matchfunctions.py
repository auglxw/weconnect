from telegram import Update
from telegram.ext import ContextTypes
from dbfunctions import (
    get_user,
    get_rest,
    put_waiting,
    put_room,
    exit_room,
)
from matchingalgo import compatibilityCheck


async def find_match_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    can_match = find_match(update.effective_user.id)

    await context.bot.send_message(
        update.effective_chat.id, str(update.effective_chat.id) + " " + str(update.effective_user.id))

    if not can_match:
        # Send message
        await context.bot.send_message(update.effective_chat.id, "We are finding you a match...")
    # button to exit search
        await context.bot.send_message(update.effective_chat.id, "/stopsearch to stop")


async def exit_search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(update.effective_chat.id, "Exiting...")
    exit_search(update.effective_user.id)
    # Calls the exit function?


def find_match(user_id):
    print("finding match")
    user_obj = get_user(user_id)
    rest_arr = get_rest(user_id)

    # compatibilityCheck
    compatible_user_id = compatibilityCheck(user_obj, rest_arr)
    print(compatible_user_id)

    # if None: put person in waiting room
    if not compatible_user_id:
        put_waiting(user_id)
        return False
    # if found user: give the users room_id
    else:
        put_room(user_id, compatible_user_id)
        return True


def exit_search(user_id):
    print("exiting search")
    exit_room(user_id)
