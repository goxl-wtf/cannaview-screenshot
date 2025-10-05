"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional


class ScreenshotRequest(BaseModel):
    """Request model for screenshot endpoint"""

    url: HttpUrl = Field(..., description="URL of the page to screenshot")
    width: int = Field(1920, ge=800, le=3840, description="Screenshot width in pixels")
    height: int = Field(1080, ge=600, le=2160, description="Screenshot height in pixels")
    wait_time: int = Field(
        10000, ge=0, le=60000, description="Time to wait after page load (milliseconds)"
    )
    wait_for_selector: Optional[str] = Field(
        None, description="CSS selector to wait for before screenshot"
    )
    full_page: bool = Field(False, description="Capture full scrollable page")

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.easydis.io/screen/67165080bb88c87815c851ad-screen-1",
                "width": 1920,
                "height": 1080,
                "wait_time": 10000,
                "wait_for_selector": "[data-slot='card']",
                "full_page": False,
            }
        }


class ScreenshotResponse(BaseModel):
    """Response model for screenshot endpoint"""

    success: bool = Field(..., description="Whether screenshot was successful")
    image_base64: Optional[str] = Field(None, description="Base64-encoded PNG image")
    metadata: Optional[dict] = Field(None, description="Screenshot metadata")
    error: Optional[str] = Field(None, description="Error message if failed")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "image_base64": "iVBORw0KGgoAAAANS...",
                "metadata": {
                    "capture_time_ms": 5234,
                    "product_count": 42,
                    "url": "https://www.easydis.io/screen/...",
                    "dimensions": {"width": 1920, "height": 1080},
                },
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check endpoint"""

    status: str = Field(..., description="Service health status")
    browser: str = Field(..., description="Browser type")
    uptime_seconds: int = Field(..., description="Service uptime in seconds")
