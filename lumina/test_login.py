import asyncio
from playwright.async_api import async_playwright

async def test_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        print("Testing login flow...")

        # Navigate to login
        await page.goto("http://127.0.0.1:5000/admin/login", wait_until="networkidle", timeout=10000)
        print("✓ Login page loaded")

        # Fill email
        await page.fill('input[type="email"]', "admin@lumina.local")
        print("✓ Email entered: admin@lumina.local")

        # Fill password
        await page.fill('input[type="password"]', "Admin123")
        print("✓ Password entered")

        # Submit form
        await page.click('button[type="submit"]')
        print("✓ Form submitted")

        # Wait for navigation
        try:
            await page.wait_for_url("http://127.0.0.1:5000/admin/**", timeout=5000)
            print("✓ Login successful! Redirected to admin dashboard")
            current_url = page.url
            print(f"  Current URL: {current_url}")
        except Exception as e:
            print(f"Login redirect timeout: {e}")
            # Check for error messages
            try:
                errors = await page.query_selector_all(".alert")
                if errors:
                    for error in errors:
                        text = await error.inner_text()
                        print(f"  Error message: {text}")
            except:
                pass
            print(f"  Current URL: {page.url}")

        await context.close()
        await browser.close()

asyncio.run(test_login())
