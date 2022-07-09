import pymongo
from pymongo import MongoClient
from matchingalgo import learnerOrSharer

CONNECTION_STRING = "mongodb+srv://maxtance:KgAFGM4XZPjUWaVN@weconnect.qrwlr.mongodb.net/?retryWrites=true&w=majority"
cluster = MongoClient(CONNECTION_STRING)
db = cluster["weconnectdb"]
collection = db["users"]


def user_exists(user_id):
    length = collection.count_documents(
        {"user_id": user_id, "status": "online"})
    if length == 0:
        print("user does not exist")
        return False
    print("user exists")

    return True


def insert_user(poll_type, cat_arr, user_id):
    if poll_type == "interest":
        if user_exists(user_id):
            data = list(collection.find({"user_id": user_id}))[0]
            type = learnerOrSharer(cat_arr, data["my_comms_id"])

            collection.update_one(
                {"user_id": user_id}, {
                    "$set": {"interested_comms_id": cat_arr, "type": type}}
            )

        else:
            data = {
                "user_id": user_id,
                "interested_comms_id": cat_arr,
                "my_comms_id": [],
                "status": "online",
                "type": "",
                "room_id": "",
            }
            collection.insert_one(data)

    elif poll_type == "share":
        if user_exists(user_id):
            data = list(collection.find({"user_id": user_id}))[0]
            type = learnerOrSharer(data["interested_comms_id"], cat_arr)

            collection.update_one(
                {"user_id": user_id}, {
                    "$set": {"my_comms_id": cat_arr, "type": type}}
            )

        else:
            data = {
                "user_id": user_id,
                "interested_comms_id": [],
                "my_comms_id": cat_arr,
                "status": "online",
                "type": "",
                "room_id": "",
            }
            collection.insert_one(data)
    # If have all needed data, can check and update type


def can_edit_user(user_id):
    return user_exists(user_id)


def edit_user(poll_type, cat_arr, user_id):
    print("editing user")
    collection.delete_many({"user_id": user_id, "status": "offline"})

    insert_user(poll_type, cat_arr, user_id)


def status_offline(user_id):
    collection.update_one({"user_id": user_id}, {
                          "$set": {"status": "offline"}})
