from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
def obtener_redes_sociales_selenium(url):
    print("Selenium")
    options = Options()
    options.add_argument('--headless') 
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    redes_sociales = []
    elementos_redes_sociales = driver.find_elements(By.XPATH, "//a[contains(@href, 'facebook.com') or contains(@href, 'twitter.com') or contains(@href, 'youtube.com') or contains(@href, 'instagram.com')]")

    for elemento in elementos_redes_sociales:
        redes_sociales.append(elemento.get_attribute("href"))

    driver.quit()
    return redes_sociales

# Ejemplo de uso
url_pagina = "https://www.coca-cola.com/es/es"
redes_sociales_selenium = obtener_redes_sociales_selenium(url_pagina)
print("Redes sociales (Selenium):", redes_sociales_selenium)


