import asyncio
import socketio

class SocketIO:
    def __init__(self) -> None:
        self.sio = socketio.AsyncClient(logger=True)
        
        @self.sio.event
        async def connect():
            print('Connection established')

        @self.sio.event
        async def connect_error(data):
            print("Connection failed")

        @self.sio.event
        async def disconnect():
            print("Disconnected")

    async def connect(self):
        await self.sio.connect('http://0.0.0.0:8080', wait_timeout = 10)
        await self.sio.wait()
    
    async def disconnect(self):
        await self.sio.disconnect()
    
    async def beginChat(self, room_id):
        await self.sio.emit("begin_chat", room_id)

    async def sendMessage(self, msg, room_id, chat_id):
        await self.sio.emit("send_message", {"room_id": room_id, "chat_id": chat_id, "msg": msg})
    
    async def exitChat(self, room_id):
        await self.sio.emit("exit_chat", room_id)


if __name__ == '__main__':
    solution = SocketIO()
    asyncio.run(solution.connect())
    # asyncio.run(SocketIO.beginChat("123"))
    # asyncio.run(SocketIO.sendMessage("Hello world", "123"))
    # asyncio.run(SocketIO.disconnect())
