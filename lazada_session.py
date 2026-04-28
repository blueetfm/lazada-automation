import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def create_session():
    async with Stealth().use_async(async_playwright()) as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir="./lazada_session", 
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--use-fake-ui-for-media-stream",
                "--use-fake-device-for-media-stream",
                "--no-sandbox",
                "--disable-infobars",
                "--window-position=0,0",
                "--ignore-certificate-errors",
            ],
            ignore_default_args=["--enable-automation"] 
        )
        
        page = await context.new_page()

        
        # This makes the browser report a real resolution and core count
        await page.add_init_script("""
            Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
            Object.defineProperty(navigator, 'deviceMemory', { get: () => 8 });
        """)
        
        await page.goto("https://member.lazada.sg/user/login")

        print("PLEASE MANUALLY LOG IN NOW.")
        print("Once you are on the home page and logged in, come back here and press Enter.")
        
        # This keeps the browser open until you press Enter in the terminal
        input("Press Enter after you have successfully logged in and solved any CAPTCHAs...")
        
        await context.close()

if __name__ == "__main__":
    asyncio.run(create_session())