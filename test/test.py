import websockets, asyncio
import time
import flask


async def hello(i):
    async with websockets.connect('ws://localhost:5000/greetings') as websocket:
        await websocket.send(str(i))
        # print("Answer for question 1?")
        question= await websocket.recv()
        # while True:
            # question = await websocket.recv()
            # if question != None:
            #     break
        print(question)
        # name = input()

        # await websocket.send(name)
        #print(f"Input Sent:- {name}")

        # greeting = await websocket.recv()
        
        # print(f"Message fromt the server: {greeting}")
        # question=None
        # if greeting == "Wrong!":
        #     return False
        # else:
        #     return True
        #websocket.close()


for i in range(10):
    result = asyncio.get_event_loop().run_until_complete(hello(i))
    if result == False:
        break


