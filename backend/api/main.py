"""FastAPI application main entry point."""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import logging

from core import get_settings, init_db, get_db, logger
from orchestrator import TaskManager
from memory import get_vector_store

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI app
settings = get_settings()
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global task manager (will be initialized on startup)
task_manager: TaskManager = None


@app.on_event("startup")
async def startup_event():
    """Initialize database and services on startup."""
    global task_manager
    
    logger.info("Starting Helios API...")
    
    # Initialize database
    init_db()
    logger.info("Database initialized")
    
    # Initialize vector store
    try:
        get_vector_store()
        logger.info("Vector store initialized")
    except Exception as e:
        logger.warning(f"Vector store initialization warning: {e}")
    
    # Initialize task manager
    db = SessionLocal()
    task_manager = TaskManager(db)
    logger.info("Task manager initialized")
    
    logger.info("Helios API started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Shutting down Helios API...")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Helios API",
        "version": settings.API_VERSION,
    }


@app.get("/api/status")
async def api_status():
    """Get API status."""
    return {
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "database_url": "configured" if settings.DATABASE_URL else "not configured",
        "vector_store_enabled": settings.ENABLE_VECTOR_STORE,
    }


# Import routes
from api.routes import tasks, business, agents, voice, websocket_video

# Include routers
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(business.router, prefix="/api/business", tags=["business"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(voice.router)
app.include_router(websocket_video.router)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
