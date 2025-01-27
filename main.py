from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from datetime import datetime
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.info("Request been invoked")
    logger.info(datetime.now())
    return {"message": "Hello World"}
