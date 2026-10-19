"""
FastAPI Server Entry Point for Unique Character Quest
-----------------------------------------------------
Initializes database tables, configures CORS, mounts REST and WebSocket routers,
and handles lifespan startup/shutdown events.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import init_db
from .api.routes import api_router
from .multiplayer.websocket import ws_router

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("backend.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler: safely initializes SQLite tables on startup."""
    logger.info("Initializing Unique Character Quest SQLite database...")
    try:
        init_db()
        logger.info("Database schema initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    yield
    logger.info("Unique Character Quest server shutting down.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API and WebSocket engine for Unique Character Quest capstone project.",
    lifespan=lifespan
)

# CORS Middleware for Streamlit and external frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits local Streamlit and remote cross-device testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(api_router, prefix="/api/v1")
app.include_router(api_router, prefix="/api")  # Convenience alias
app.include_router(ws_router)


@app.get("/")
def read_root():
    """Root metadata endpoint."""
    return {
        "title": "Unique Character Quest API",
        "version": settings.APP_VERSION,
        "description": "Educational capstone game backend centered on the First Non-Repeating Character algorithm.",
        "documentation": "/docs",
        "status": "online"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=True)
