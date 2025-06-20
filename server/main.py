﻿from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.presentation.controllers import recommendations_router, websocket_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommendations_router)
app.include_router(websocket_router)
