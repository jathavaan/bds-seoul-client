from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

websocket_router = APIRouter()
connected_clients: list[WebSocket] = []


@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
