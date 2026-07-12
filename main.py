from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected")
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received: {data}")
            await websocket.send_text(data)
            logger.info(f"Echoed back: {data}")
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    finally:
        try:
            await websocket.close()
        except RuntimeError:
            # Socket already closed (e.g. after disconnect)
            pass


@app.get("/")
async def root(event: str = None):
    logger.info(f"GET / called with event={event} at {datetime.now()}")
    return {
        "message": "Echo test API is running",
        "you_sent": event,
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/echo")
async def echo_post(payload: dict):
    logger.info(f"POST /echo received payload: {payload}")
    return {
        "you_sent": payload,
        "timestamp": datetime.now().isoformat(),
    }
