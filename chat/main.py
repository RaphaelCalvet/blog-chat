from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime
import json
import redis.asyncio as redis
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.redis = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        messages = await self.get_messages()
        for message in messages:
            await websocket.send_text(message)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def save_message(self, message: str):
        if self.redis:
            await self.redis.rpush("chat_messages", message)

    async def get_messages(self) -> List[str]:
        if self.redis:
            messages = await self.redis.lrange("chat_messages", 0, -1)
            return [msg.decode('utf-8') for msg in messages]
        return []

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def read_items(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.on_event("startup")
async def startup_event():
    manager.redis = await redis.from_url("redis://localhost")

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    try:
        while True:
            data = await websocket.receive_text()
            message = {"time": current_time, "clientId": client_id, "message": data}
            message_json = json.dumps(message)
            await manager.broadcast(message_json)
            await manager.save_message(message_json)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
