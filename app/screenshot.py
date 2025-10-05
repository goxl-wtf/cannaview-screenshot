"""
Screenshot capture service using Playwright
"""
import base64
import time
import logging
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Browser, Page

logger = logging.getLogger(__name__)


class ScreenshotService:
    """Manages browser instance and screenshot capture"""

    def __init__(self):
        self.browser: Optional[Browser] = None
        self.playwright = None

    async def initialize(self):
        """Initialize Playwright and browser"""
        if not self.playwright:
            logger.info("🚀 Initializing Playwright...")
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)
            logger.info("✅ Browser initialized successfully")

    async def cleanup(self):
        """Clean up browser and Playwright"""
        if self.browser:
            await self.browser.close()
            logger.info("🔒 Browser closed")

        if self.playwright:
            await self.playwright.stop()
            logger.info("🔒 Playwright stopped")

    async def capture_screenshot(
        self,
        url: str,
        width: int = 1920,
        height: int = 1080,
        wait_time: int = 10000,
        wait_for_selector: Optional[str] = None,
        full_page: bool = False,
    ) -> Dict[str, Any]:
        """
        Capture a screenshot of the given URL

        Args:
            url: URL to screenshot
            width: Viewport width
            height: Viewport height
            wait_time: Time to wait after page load (ms)
            wait_for_selector: CSS selector to wait for
            full_page: Whether to capture full scrollable page

        Returns:
            Dict with success, image_base64, metadata, or error
        """
        start_time = time.time()
        page: Optional[Page] = None

        try:
            await self.initialize()

            if not self.browser:
                raise Exception("Browser not initialized")

            # Create new page
            page = await self.browser.new_page(
                viewport={"width": width, "height": height}
            )

            logger.info(f"📍 Navigating to: {url}")

            # Navigate to URL
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)

            logger.info("✅ Page loaded")

            # Wait for specific selector if provided
            if wait_for_selector:
                logger.info(f"⏳ Waiting for selector: {wait_for_selector}")
                try:
                    await page.wait_for_selector(wait_for_selector, timeout=30000)
                    logger.info("✅ Selector found")
                except Exception as e:
                    logger.warning(f"⚠️  Selector not found: {e}")

            # Additional wait time for dynamic content
            if wait_time > 0:
                logger.info(f"⏱️  Waiting {wait_time}ms for content to render...")
                await page.wait_for_timeout(wait_time)

            # Count products if selector was provided
            product_count = 0
            if wait_for_selector:
                product_count = await page.evaluate(
                    f'document.querySelectorAll("{wait_for_selector}").length'
                )
                logger.info(f"📊 Found {product_count} elements matching selector")

            # Capture screenshot
            logger.info("📸 Capturing screenshot...")
            screenshot_bytes = await page.screenshot(type="png", full_page=full_page)

            # Encode to base64
            image_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")

            capture_time = int((time.time() - start_time) * 1000)

            logger.info(f"✅ Screenshot captured in {capture_time}ms ({len(screenshot_bytes)} bytes)")

            return {
                "success": True,
                "image_base64": image_base64,
                "metadata": {
                    "capture_time_ms": capture_time,
                    "image_size_bytes": len(screenshot_bytes),
                    "url": url,
                    "dimensions": {"width": width, "height": height},
                    "product_count": product_count if wait_for_selector else None,
                },
            }

        except Exception as e:
            logger.error(f"❌ Screenshot failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "metadata": {
                    "capture_time_ms": int((time.time() - start_time) * 1000),
                    "url": url,
                },
            }

        finally:
            if page:
                await page.close()


# Singleton instance
screenshot_service = ScreenshotService()
