"""
CannaView Screenshot Service
FastAPI application for capturing screenshots of EasyDis digital display screens
"""
import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.models import ScreenshotRequest, ScreenshotResponse, HealthResponse
from app.screenshot import screenshot_service
from app.auth import verify_api_key
from app.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Track service start time
SERVICE_START_TIME = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting CannaView Screenshot Service...")
    await screenshot_service.initialize()
    logger.info("✅ Service ready")

    yield

    # Shutdown
    logger.info("🔒 Shutting down service...")
    await screenshot_service.cleanup()
    logger.info("👋 Service stopped")


# Create FastAPI app
app = FastAPI(
    title="CannaView Screenshot Service",
    description="Dedicated screenshot service for EasyDis digital display screens using Playwright",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Info"])
async def root():
    """Root endpoint - service information"""
    return {
        "service": "CannaView Screenshot Service",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    uptime = int(time.time() - SERVICE_START_TIME)

    return HealthResponse(
        status="healthy",
        browser=settings.BROWSER_TYPE,
        uptime_seconds=uptime,
    )


@app.post("/screenshot", response_model=ScreenshotResponse, tags=["Screenshot"])
async def take_screenshot(
    request: ScreenshotRequest,
    api_key: str = Depends(verify_api_key),
):
    """
    Capture a screenshot of the specified URL

    Requires X-API-Key header for authentication.
    """
    url_str = str(request.url)

    # Verify domain is allowed
    if not settings.is_domain_allowed(url_str):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Domain not allowed. Allowed domains: {settings.ALLOWED_DOMAINS}",
        )

    logger.info(f"📸 Screenshot request: {url_str}")

    # Capture screenshot
    result = await screenshot_service.capture_screenshot(
        url=url_str,
        width=request.width,
        height=request.height,
        wait_time=request.wait_time,
        wait_for_selector=request.wait_for_selector,
        full_page=request.full_page,
    )

    if not result["success"]:
        logger.error(f"❌ Screenshot failed: {result.get('error')}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Screenshot capture failed"),
        )

    return ScreenshotResponse(**result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
