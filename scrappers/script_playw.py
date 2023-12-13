import asyncio
from playwright.async_api import async_playwright

async def obtener_redes_sociales_playwright(url):
    async with async_playwright() as p:
        #browser = await p.chromium.launch(headless=False) # Abre una ventana
        browser = await p.chromium.launch() # No abre una ventana
        page = await browser.new_page()
        await page.goto(url)

        redes_sociales = await page.query_selector_all("a[href*='facebook.com'], a[href*='twitter.com'], a[href*='instagram.com']")

        resultados = [await red_social.get_attribute("href") for red_social in redes_sociales]

        await browser.close()

    return resultados

async def main():
    url_pagina = "https://www.nike.com/es/"
    redes_sociales_playwright = await obtener_redes_sociales_playwright(url_pagina)
    print("Redes sociales (Playwright):", redes_sociales_playwright)

if __name__ == "__main__":
    asyncio.run(main())
