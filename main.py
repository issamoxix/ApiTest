from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio

app = FastAPI()

names = ["John", "Jane", "Bob", "Alice"]
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            for name in names:
                await websocket.send_text(name)
                await asyncio.sleep(1)
            break
    except WebSocketDisconnect:
        print("Client disconnected")
    finally:
        await websocket.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}