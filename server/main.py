from fastapi import FastAPI

from src.presentation.controllers import recommendations_router

app = FastAPI()
app.include_router(recommendations_router)
