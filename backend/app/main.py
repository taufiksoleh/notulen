from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from pathlib import Path

from app.core.config import settings
from app.api.routes import router
from app.models import Base, engine

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Speech-to-Text API for Indonesian Meeting Notes",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
logger.info("Creating database tables...")
Base.metadata.create_all(bind=engine)

# Create necessary directories
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path("./data").mkdir(parents=True, exist_ok=True)

# Include routers
app.include_router(router, prefix=settings.API_V1_STR, tags=["meetings"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Notulen API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.on_event("startup")
async def startup_event():
    """Run on startup"""
    logger.info(f"Starting {settings.APP_NAME}...")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Upload directory: {settings.UPLOAD_DIR}")
    logger.info(f"Whisper model: {settings.WHISPER_MODEL}")
    logger.info(f"Use Indonesian model: {settings.USE_INDONESIAN_MODEL}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on shutdown"""
    logger.info("Shutting down Notulen API...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
