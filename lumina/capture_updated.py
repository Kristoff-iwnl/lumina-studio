import asyncio
from playwright.async_api import async_playwright
import os

async def capture_updated():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        viewports = [
            (360, 800, "mobile"),
            (768, 1024, "tablet"),
            (1280, 720, "desktop"),
        ]

        os.makedirs("docs/updated", exist_ok=True)

        for width, height, label in viewports:
            context = await browser.new_context(viewport={"width": width, "height": height})
            page = await context.new_page()

            try:
                # Wait for animations to load
                await page.goto("http://127.0.0.1:5000/", wait_until="networkidle", timeout=10000)
                # Wait a bit for aurora animation to start
                await page.wait_for_timeout(2000)
                await page.screenshot(path=f"docs/updated/homepage-{label}.png")
                print(f"✓ Homepage with aurora ({label}): docs/updated/homepage-{label}.png")
            except Exception as e:
                print(f"✗ Error on {label}: {e}")

            await context.close()

        await browser.close()
        print("\n✅ Updated screenshots captured")

asyncio.run(capture_updated())
