import asyncio
from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

websocket_router = APIRouter()
connected_clients: list[WebSocket] = []


@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    async def send_periodic():
        try:
            while True:
                await asyncio.sleep(1)
                await websocket.send_text("Hello from server!")
        except (WebSocketDisconnect, asyncio.CancelledError):
            pass

    send_task = asyncio.create_task(send_periodic())

    try:
        while True:
            await websocket.receive_text()  # Keep the connection alive
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        send_task.cancel()
        try:
            await send_task
        except asyncio.CancelledError:
            pass
