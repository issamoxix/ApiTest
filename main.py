from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from time import sleep

app = FastAPI()

names = ["John", "Jane", "Bob", "Alice"]
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        for name in names:
            await websocket.send_text(name)
            sleep(1)
    except WebSocketDisconnect:
        print("Client disconnected")
    finally:
        await websocket.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}