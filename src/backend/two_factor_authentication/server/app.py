"""
FastAPI application setting
"""


from fastapi import FastAPI

from src.backend.server.routes import router

app = FastAPI()
app.include_router(router)
