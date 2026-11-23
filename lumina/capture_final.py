import asyncio
from playwright.async_api import async_playwright
import os

async def capture_final():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        viewports = [
            (360, 2000, "mobile"),
            (768, 2000, "tablet"),
            (1280, 1400, "desktop"),
        ]

        os.makedirs("docs/final", exist_ok=True)

        for width, height, label in viewports:
            context = await browser.new_context(viewport={"width": width, "height": height})
            page = await context.new_page()

            try:
                # Capture full page
                await page.goto("http://127.0.0.1:5000/", wait_until="networkidle", timeout=10000)
                # Wait for animations
                await page.wait_for_timeout(2000)
                await page.screenshot(path=f"docs/final/full-page-{label}.png", full_page=True)
                print(f"✓ Full page ({label}): docs/final/full-page-{label}.png")
            except Exception as e:
                print(f"✗ Error on {label}: {e}")

            await context.close()

        await browser.close()
        print("\n✅ Final screenshots captured with aurora palette & spacing")

asyncio.run(capture_final())
