import asyncio
from playwright.async_api import async_playwright

async def test_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        print("Testing login flow with admin@lumina.com...")

        # Navigate to login
        await page.goto("http://127.0.0.1:5000/admin/login", wait_until="networkidle", timeout=10000)
        print("✓ Login page loaded")

        # Fill email
        await page.fill('input[name="email"]', "admin@lumina.com")
        print("✓ Email entered: admin@lumina.com")

        # Fill password
        await page.fill('input[name="password"]', "Admin123")
        print("✓ Password entered")

        # Submit form
        await page.click('button[type="submit"]')
        print("✓ Form submitted")

        # Wait for navigation
        try:
            await page.wait_for_url("**/admin/**", timeout=5000)
            print(f"✓ Login successful! Redirected to {page.url}")
        except Exception as e:
            print(f"Login timeout or failed: {e}")
            print(f"Current URL: {page.url}")
            try:
                errors = await page.query_selector_all(".alert")
                for err in errors:
                    print(f"  Alert: {await err.inner_text()}")
            except:
                pass

        await context.close()
        await browser.close()

asyncio.run(test_login())
