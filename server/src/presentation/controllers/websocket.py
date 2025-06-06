import asyncio
from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from src.application import Container

websocket_router = APIRouter()
connected_clients: list[WebSocket] = []

container = Container()
process_status_consumer = container.process_status_consumer()


@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    async def publish_consumer():
        while True:
            success, result = await asyncio.to_thread(process_status_consumer.consume)
            if success and result is not None:
                await websocket.send_json({
                    "game_id": int(result.get("game_id")),
                    "type": result.get("type"),
                    "status": result.get("status"),
                })

            await asyncio.sleep(0.1)

    publish_task = asyncio.create_task(publish_consumer())

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        publish_task.cancel()
