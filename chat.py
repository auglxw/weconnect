import asyncio
import socketio

class SocketIO:
    sio = socketio.AsyncClient(logger=True)

    @sio.event
    async def connect():
        print('Connection established')

    @sio.event
    async def connect_error(data):
        print("Connection failed")

    @sio.event
    async def disconnect():
        print("Disconnected")

    async def connect():
        await SocketIO.sio.connect('http://0.0.0.0:8080', wait_timeout = 10)
        # await SocketIO.sio.wait()
    
    async def disconnect():
        await SocketIO.sio.disconnect()
    
    async def beginChat(room_id):
        await SocketIO.sio.emit("begin_chat", room_id)

    async def sendMessage(msg, room_id, chat_id):
        await SocketIO.sio.emit("send_message", {"room_id": room_id, "chat_id": chat_id, "msg": msg})
    
    async def exitChat(room_id):
        await SocketIO.sio.emit("exit_chat", room_id)


if __name__ == '__main__':
    asyncio.run(SocketIO.connect())
    # asyncio.run(SocketIO.beginChat("123"))
    # asyncio.run(SocketIO.sendMessage("Hello world", "123"))
    # asyncio.run(SocketIO.disconnect())
