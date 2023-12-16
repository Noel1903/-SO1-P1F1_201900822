import time
from playwright.sync_api import sync_playwright

def obtener_likes_con_xpath(url, xpath):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        # Agregar tiempo de espera para que la página cargue completamente
        time.sleep(5)  # Puedes ajustar este valor según sea necesario

        # Obtener el texto que contiene la información de "Me gusta" utilizando XPath
        likes_text = page.inner_text(f'xpath={xpath}')

        # Imprimir la cantidad de "Me gusta"
        print("subs YT",likes_text)

        browser.close()

# URL de ejemplo y XPath
url_ejemplo = "https://www.youtube.com/CocaColaJourneyES"
xpath_ejemplo = '//*[@id="subscriber-count"]'

obtener_likes_con_xpath(url_ejemplo, xpath_ejemplo)