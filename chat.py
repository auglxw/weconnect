import asyncio
import socketio

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('connection established')

async def main():
    await sio.connect('http://0.0.0.0:8080', wait_timeout = 10)
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())
