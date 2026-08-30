"""Main FastAPI application for Market Mind Pro."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.api.ai_router import router as ai_router
from app.api.data_router import router as data_router
from app.core.config import settings


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
    )

    # Set all CORS enabled
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify exact origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include main API router
    app.include_router(api_router)
    
    # Include AI analytics router
    app.include_router(ai_router)
    
    # Include stock data router
    app.include_router(data_router)

    @app.get("/")
    def root():
        """Root endpoint."""
        return {"message": "Welcome to Market Mind Pro API"}

    @app.get("/health")
    def health():
        """Health check endpoint."""
        return {"status": "ok"}

    return app


app = create_app()
