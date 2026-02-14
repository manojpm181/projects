from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from src.core.config import settings
from src.api.v1.router import api_router
from src.middleware.rate_limit import RateLimitMiddleware
from src.middleware.request_id import RequestIDMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown."""
    
    # Startup
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"📊 Environment: {settings.ENVIRONMENT}")
    logger.info(f"🤖 Default Model: {settings.DEFAULT_MODEL}")
    logger.info(f"⚡ Rate Limit: {settings.RATE_LIMIT_REQUESTS}/{settings.RATE_LIMIT_PERIOD}s")
    logger.info("✅ All systems ready")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="100% FREE AI Conversation API with Groq + Supabase",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(RequestIDMiddleware)
app.add_middleware(RateLimitMiddleware)

# Include routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "description": "100% FREE AI Conversation API",
        "features": [
            "✅ Groq LLM (FREE, 30 req/min)",
            "✅ Supabase Auth & Database (FREE)",
            "✅ Real-time streaming (SSE)",
            "✅ Rate limiting (in-memory)",
            "✅ JWT authentication",
            "✅ Conversation management",
            "✅ Token counting (approximate)",
        ],
        "documentation": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )