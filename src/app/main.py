from fastapi import FastAPI

from app.controllers.api import api_router

app = FastAPI()

app.include_router(api_router)
