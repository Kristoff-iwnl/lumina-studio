"""
Capture after screenshots and measure performance improvements
"""
import asyncio
from playwright.async_api import async_playwright
import json
from pathlib import Path

async def capture_after_screenshots():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        # Create docs/after directory
        Path("docs/after").mkdir(parents=True, exist_ok=True)

        await page.goto("http://127.0.0.1:5000", wait_until="networkidle")

        # Capture at 4 widths
        widths = [360, 768, 1280, 1920]
        for width in widths:
            await page.set_viewport_size({"width": width, "height": 1200})
            await page.screenshot(path=f"docs/after/homepage-{width}px.png", full_page=True)
            print(f"✓ Captured homepage after at {width}px")

        # Capture login page
        await page.goto("http://127.0.0.1:5000/auth/login", wait_until="networkidle")
        for width in [360, 768, 1280]:
            await page.set_viewport_size({"width": width, "height": 800})
            await page.screenshot(path=f"docs/after/login-{width}px.png", full_page=True)
            print(f"✓ Captured login after at {width}px")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_after_screenshots())
