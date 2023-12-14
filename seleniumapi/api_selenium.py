from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import requests
import json
#import redis
#from rsmq import RedisSMQ

node_url = 'http://nodejs_app:6000/data'

def obtener_redes_sociales_selenium(url):
    print("Selenium")
    options = Options()
    options.binary_location = '/usr/bin/firefox'
    #options.headless = True
    options.add_argument('--headless') 
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    try:
        
        driver = webdriver.Firefox(options=options)
        driver.get(url)

        redes_sociales = []
        elementos_redes_sociales = driver.find_elements(By.XPATH, "//a[contains(@href, 'facebook.com') or contains(@href, 'twitter.com') or contains(@href, 'linkedin.com') or contains(@href, 'youtube.com') or contains(@href, 'instagram.com')]")

        for elemento in elementos_redes_sociales:
            redes_sociales.append(elemento.get_attribute("href"))

        driver.quit()
        return redes_sociales

    except Exception as e:
        print("Error al obtener las redes sociales con Selenium")
        print(e)
        return []

def enviar_a_redis_rsmq(informacion):
    data = {"data": informacion}
    response = requests.post(node_url, json=data)
    print(response.text)
    #redis_client = redis.StrictRedis(host='172.17.0.2', port=6379, decode_responses=True)

    #redis_client.set("mi_clave", informacion)
    #print("Información almacenada directamente en Redis.")

url_pagina = "https://www.coca-cola.com/es/es"
redes_sociales_selenium = obtener_redes_sociales_selenium(url_pagina)
print("Redes sociales (Selenium):", redes_sociales_selenium)
 # Enviar la información a Redis RSMQ
informacion = "\n".join(redes_sociales_selenium)
enviar_a_redis_rsmq(informacion)
url_pagina = "https://www.intelaf.com/"
redes_sociales_selenium = obtener_redes_sociales_selenium(url_pagina)
print("Redes sociales (Selenium):", redes_sociales_selenium)
 # Enviar la información a Redis RSMQ
informacion = "\n".join(redes_sociales_selenium)
enviar_a_redis_rsmq(informacion)
url_pagina = "https://www.tacobell.com.gt/index.html"
redes_sociales_selenium = obtener_redes_sociales_selenium(url_pagina)
print("Redes sociales (Selenium):", redes_sociales_selenium)
# Enviar la información a Redis RSMQ
informacion = "\n".join(redes_sociales_selenium)
enviar_a_redis_rsmq(informacion)

