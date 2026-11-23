"""
Capture login page screenshots after redesign in multiple states
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
            # 1. Empty form
            await page.goto("http://127.0.0.1:5000/auth/login", wait_until="networkidle")
            await page.set_viewport_size({"width": width, "height": 800})
            await page.screenshot(path=f"docs/after/login-empty-{width}px.png")
            print(f"✓ Login empty at {width}px")

            # 2. Focus state (click email field)
            await page.click("#email")
            await page.screenshot(path=f"docs/after/login-focus-{width}px.png")
            print(f"✓ Login focus at {width}px")

            # 3. Filled state
            await page.fill("#email", "test@example.com")
            await page.fill("#password", "password123")
            await page.screenshot(path=f"docs/after/login-filled-{width}px.png")
            print(f"✓ Login filled at {width}px")

            # 4. Password visible toggle
            await page.click(".password-toggle")
            await page.screenshot(path=f"docs/after/login-password-visible-{width}px.png")
            print(f"✓ Login password visible at {width}px")

        # 5. Test error state (wrong credentials)
        await page.goto("http://127.0.0.1:5000/auth/login", wait_until="networkidle")
        await page.set_viewport_size({"width": 768, "height": 900})
        await page.fill("#email", "admin@lumina.local")
        await page.fill("#password", "WrongPassword")
        await page.click("#submit-btn")
        await page.wait_for_timeout(2000)  # Wait for response
        await page.screenshot(path=f"docs/after/login-error-768px.png")
        print(f"✓ Login error state at 768px")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_login_screenshots())
