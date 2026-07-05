"""
FastAPI application setting
"""


from fastapi import FastAPI

from src.backend.two_factor_authentication.server.routes import router

app = FastAPI()
app.include_router(router)
