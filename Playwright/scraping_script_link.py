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
        print("seguidores likedin",likes_text)

        browser.close()

# URL de ejemplo y XPath
url_ejemplo = "https://www.linkedin.com/company/taco-bell-guatemala/"
xpath_ejemplo = '/html/body/main/section[1]/section/div/div[2]/div[1]/h3'

obtener_likes_con_xpath(url_ejemplo, xpath_ejemplo)