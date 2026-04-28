import asyncio
import datetime

from playwright.async_api import async_playwright, TimeoutError
from playwright_stealth import Stealth
import random
import time

POKEMON_URL = "https://www.lazada.sg/products/pokemon-trading-card-game-mega-evolution-ascended-heroes-booster-bundle-limit-1-per-person-i13696744288-s124594658123.html?dsource=share&laz_share_info=3421846226_0_100_551484_3421848226_null&laz_token=8472e6970d54198da7a07e41d46fa038&exlaz=d_2%3Amm_181550867_184852003_2143452003%3Asg2339018%3A00%3A%7B%22generateType%22%3A%221%22%2C%22itemId%22%3A%2213696744288%22%2C%22sellerId%22%3A%221628720011%22%2C%22appSourcePage%22%3A%22lzd_homesite_app_share_product%22%2C%22affiliateOfferId%22%3A%22sg2339018%22%2C%22generateTimestamp%22%3A%221776996843882%22%2C%22appSourceModule%22%3A%22lzd_homesite_app_share_product_module%22%2C%22platform%22%3A%223%22%2C%22skuId%22%3A%22124594658123%22%7D"
USER_DATA_DIR = "/lazada_session"

# https://www.browserstack.com/guide/playwright-captcha
'''
button html:
<button type="button" class="iweb-button iweb-button-secondary add-to-cart-buy-now-btn   add-to-cart-buy-now-btn  "><div class="iweb-button-mask" data-spm-anchor-id="a2o42.pdp_revamp.0.i1.30b3225eVajyJN"></div><span class="pdp-button-text"><span class="">Buy Now</span></span></button>

'''

async def generate_random_behavior(page) -> None:
    x = random.randint(100, 800)
    y = random.randint(100, 600)
    await page.mouse.move(x, y)

    delta = random.randint(-300, 300)
    await page.evaluate(f'window.scrollBy(0, {delta})')

    await asyncio.sleep(random.uniform(0.3, 0.7))


async def purchase() -> None:
    async with Stealth().use_async(async_playwright()) as p:
        # 1. launch context
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False, # Keep False to solve CAPTCHAs manually if needed
            args=["--disable-blink-features=AutomationControlled"]
        )

        # 2. navigating to the page
        page = await context.new_page()


        print(f"[{datetime.now()}] Navigating to Lazada...")
        await page.goto(POKEMON_URL, wait_until="domcontentloaded")

        # 3. loop to check 
        bought = False
        while not bought:
            try:
                buy_now_btn = page.get_by_text("Buy Now", exact=False)
                
                if await buy_now_btn.is_visible(timeout=2000):
                    print("!!! ITEM IN STOCK !!!")
                    await buy_now_btn.click()
                    bought = True
                else:
                    raise TimeoutError
                    
            except (TimeoutError, Exception):
                print("Item out of stock.")
                break

        await asyncio.sleep(100) 

    return

if __name__ == "__main__":
    asyncio.run(purchase())
