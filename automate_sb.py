import asyncio
from playwright.async_api import async_playwright
from seleniumbase import cdp_driver

POKEMON_URL = "https://www.lazada.sg/products/pokemon-trading-card-game-mega-evolution-ascended-heroes-booster-bundle-limit-1-per-person-i13696744288-s124594658123.html?dsource=share&laz_share_info=3421846226_0_100_551484_3421848226_null&laz_token=8472e6970d54198da7a07e41d46fa038&exlaz=d_2%3Amm_181550867_184852003_2143452003%3Asg2339018%3A00%3A%7B%22generateType%22%3A%221%22%2C%22itemId%22%3A%2213696744288%22%2C%22sellerId%22%3A%221628720011%22%2C%22appSourcePage%22%3A%22lzd_homesite_app_share_product%22%2C%22affiliateOfferId%22%3A%22sg2339018%22%2C%22generateTimestamp%22%3A%221776996843882%22%2C%22appSourceModule%22%3A%22lzd_homesite_app_share_product_module%22%2C%22platform%22%3A%223%22%2C%22skuId%22%3A%22124594658123%22%7D"

'''
button html:
<button type="button" class="iweb-button iweb-button-secondary add-to-cart-buy-now-btn   add-to-cart-buy-now-btn  "><div class="iweb-button-mask" data-spm-anchor-id="a2o42.pdp_revamp.0.i1.30b3225eVajyJN"></div><span class="pdp-button-text"><span class="">Buy Now</span></span></button>

'''

async def main():
    driver = await cdp_driver.start_async(browser="chrome", headless=False)
    endpoint_url = driver.get_endpoint_url()

    try:
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(endpoint_url)
            context = browser.contexts[0]
            page = context.pages[0]

            print("Navigating to Lazada...")
            await page.goto(POKEMON_URL, wait_until="domcontentloaded")

            print("Checking for CAPTCHA...")
            await driver.solve_captcha() 
            
            print("Monitoring for 'Buy Now' button...")
            while True:
                # Check via Playwright locator
                # # lazada has 2 same-named buttons, the first is the Buy Now button
                buy_now = page.locator(".add-to-cart-buy-now-btn").first
                
                if await buy_now.is_visible(timeout=2000):
                    print("!!! SUCCESS: BUY NOW DETECTED !!!")
                    # You can add a sound here or await page.pause() to take over
                    break
                else:
                    print("Not found yet... checking again.")
                    await asyncio.sleep(5)
                    
            # Keep open for manual purchase
            await asyncio.sleep(1000) 

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await driver.quit()

if __name__ == "__main__":
    asyncio.run(main())