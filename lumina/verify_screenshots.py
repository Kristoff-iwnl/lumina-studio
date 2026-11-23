import asyncio
from playwright.async_api import async_playwright
import os

async def capture_screenshots():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        # Viewport sizes to test
        viewports = [
            (360, 800, "mobile"),
            (768, 1024, "tablet"),
            (1280, 720, "desktop"),
        ]

        os.makedirs("docs/verify", exist_ok=True)

        for width, height, label in viewports:
            context = await browser.new_context(viewport={"width": width, "height": height})
            page = await context.new_page()

            try:
                # Capture homepage
                await page.goto("http://127.0.0.1:5000/", wait_until="networkidle", timeout=10000)
                await page.screenshot(path=f"docs/verify/homepage-{label}.png")
                print(f"✓ Homepage ({label}): docs/verify/homepage-{label}.png")
            except Exception as e:
                print(f"✗ Homepage ({label}): {e}")

            try:
                # Capture login page
                await page.goto("http://127.0.0.1:5000/admin/login", wait_until="networkidle", timeout=10000)
                await page.screenshot(path=f"docs/verify/login-{label}.png")
                print(f"✓ Login ({label}): docs/verify/login-{label}.png")
            except Exception as e:
                print(f"✗ Login ({label}): {e}")

            await context.close()

        await browser.close()
        print("\n✅ Screenshot verification complete")

asyncio.run(capture_screenshots())
