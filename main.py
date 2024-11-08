from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if data.lower() == "exit":
                await websocket.send_text("Goodbye!")
                break
            await websocket.send_json({"message": data})
    except WebSocketDisconnect:
        print("Client disconnected")
    finally:
        await websocket.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}