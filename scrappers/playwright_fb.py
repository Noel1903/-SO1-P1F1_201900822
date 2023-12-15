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
        likes_text = page.locator(f'xpath={xpath}').highlight()

        # Imprimir la cantidad de "Me gusta"
        print(likes_text)

        browser.close()

# URL de ejemplo y XPath
url_ejemplo = "https://www.facebook.com/CocaColaCoEspana"
xpath_ejemplo = "/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a[1]"

obtener_likes_con_xpath(url_ejemplo, xpath_ejemplo)
