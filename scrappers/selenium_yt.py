from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def obtener_likes_facebook(url):
    print("Selenium")
    options = Options()
    options.add_argument('--headless') 
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    # Espera hasta que el elemento que contiene la información de likes sea visible
    try:
        element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="subscriber-count"]'))
        )
    except Exception as e:
        print(f"No se pudo encontrar el elemento: {e}")
        driver.quit()
        return None

    # Obtiene el texto que contiene la cantidad de likes
    likes_text = element.text

    driver.quit()
    return likes_text

# Ejemplo de uso
url_pagina_facebook = "https://www.youtube.com/CocaColaJourneyES"
likes_facebook = obtener_likes_facebook(url_pagina_facebook)

if likes_facebook is not None:
    print("Cantidad de youtube", likes_facebook)
else:
    print("No se pudo obtener la cantidad de likes.")
