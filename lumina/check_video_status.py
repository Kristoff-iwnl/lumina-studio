import asyncio
from playwright.async_api import async_playwright

async def check_video():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))

        await page.goto("http://127.0.0.1:5000/", wait_until="networkidle")

        video_info = await page.evaluate("""() => {
            const v = document.querySelector('.hero-bg-video');
            if (!v) return "No video element found";
            return {
                src: v.currentSrc,
                readyState: v.readyState,
                networkState: v.networkState,
                error: v.error ? v.error.code : null,
                paused: v.paused,
                ended: v.ended
            };
        }""")
        print("Video info:", video_info)

        await browser.close()

asyncio.run(check_video())
