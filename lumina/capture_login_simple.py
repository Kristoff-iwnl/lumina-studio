"""
Capture login page screenshots after redesign
"""
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def capture_login_screenshots():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        Path("docs/after").mkdir(parents=True, exist_ok=True)

        # Test widths for login
        widths = [360, 768, 1280]

        for width in widths:
            # Empty form
            await page.goto("http://127.0.0.1:5000/auth/login", wait_until="networkidle")
            await page.set_viewport_size({"width": width, "height": 900})
            await page.screenshot(path=f"docs/after/login-{width}px.png", full_page=True)
            print(f"✓ Login page captured at {width}px")

        # Error state (wrong credentials) at 768px
        await page.goto("http://127.0.0.1:5000/auth/login")
        await page.set_viewport_size({"width": 768, "height": 900})
        await page.fill("#email", "admin@lumina.local")
        await page.fill("#password", "WrongPassword")
        await page.click("#submit-btn")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=f"docs/after/login-error-768px.png", full_page=True)
        print(f"✓ Login error state captured at 768px")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_login_screenshots())
