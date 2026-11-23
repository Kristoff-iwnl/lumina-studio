import asyncio
from playwright.async_api import async_playwright
import os

async def capture_hero():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 1280, "height": 720})
        page = await context.new_page()
        os.makedirs("docs/hero_verify", exist_ok=True)
        await page.goto("http://127.0.0.1:5000/", wait_until="networkidle", timeout=10000)
        await page.wait_for_timeout(2000)
        await page.screenshot(path="docs/hero_verify/hero-video.png")
        print("✓ Hero video screenshot captured")
        await context.close()
        await browser.close()

asyncio.run(capture_hero())
