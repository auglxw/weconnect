from aiohttp import web
from telegram import Bot
from telegram.ext import Application
import socketio, os

application = Application.builder().token("5474527930:AAFAFk88EYYIfAi9YQkgvdZe_5wqg-WBAFU").build()
sio = socketio.AsyncServer(async_mode='aiohttp', logger=True)
app = web.Application()
sio.attach(app)

@sio.event
async def connect(sid, environ):
    print("Connect ", sid)

@sio.event
async def begin_chat(sid, room_id):
    sio.enter_room(sid, room_id)

@sio.event
async def exit_chat(sid, room_id):
    sio.leave_room(sid, room_id)

@sio.event
async def send_message(sid, data):
    await sio.emit("receive_message", data, room=data["room_id"], skip_sid=sid)

@sio.event
async def receive_message(sid, data):
    application.bot.send_message(data["chat_id"], data["msg"])

@sio.event
async def disconnect(sid):
    print('Disconnect ', sid)


if __name__ == '__main__':
    web.run_app(app)
