"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.v1.auth import router as auth_router

app = FastAPI(
    title="SmartCare AI API",
    version="0.1.0",
)

app.include_router(auth_router, prefix="/api/v1")
