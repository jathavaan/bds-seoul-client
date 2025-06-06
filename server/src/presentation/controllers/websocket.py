import asyncio
import logging

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from src.application import Container

websocket_router = APIRouter()
connected_clients: list[WebSocket] = []

container = Container()
logger = container.logger()
process_status_consumer = container.process_status_consumer()


@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    async def publish_consumer():
        while True:
            success, result = await asyncio.to_thread(process_status_consumer.consume)
            if success:
                game_id, process_type, process_status = result
                await websocket.send_json({
                    "gameId": game_id,
                    "type": process_type.value,
                    "status": process_status.value,
                })

            await asyncio.sleep(0.1)

    publish_task = asyncio.create_task(publish_consumer())

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        publish_task.cancel()
