from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from flask import Flask,request
import json
import re,time
import redis
#from rsmq import RedisSMQ
app = Flask(__name__)

redis_connection = redis.StrictRedis(host='172.20.0.5', port=6379, decode_responses=True)
node_url = 'http://172.17.0.1:3000/data_selenium'

pattern_facebook = re.compile(r'^https?://(?:www\.)?facebook\.com/[a-zA-Z0-9.]+/?$')
pattern_twitter = re.compile(r'^https?://(?:www\.)?twitter\.com/[a-zA-Z0-9_]+/?$')
pattern_instagram = re.compile(r'^https?://(?:www\.)?instagram\.com/[a-zA-Z0-9_.]+/?$')
pattern_youtube = re.compile(r'^https?://(?:www\.)?youtube\.com/(?:c/)?(?:[a-zA-Z0-9_-]+/)?(?:channel|user)/[a-zA-Z0-9_-]+/?$')
pattern_youtube_01 = re.compile(r'^https?://(?:www\.)?youtube\.com/(?:c/|C/)?[a-zA-Z0-9_-]+/?$')
pattern_linkedin = re.compile(r'^https?://(?:www\.)?linkedin\.com/company/[a-zA-Z0-9_-]+/?$')


#Metodo para obtener los seguidores de linkedin
def obtener_cantidad_seguidores_linkedin(url):
    print("Selenium")
    options = Options()
    options.add_argument('--headless') 
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    # Espera hasta que el elemento que contiene la información de likes sea visible
    try:
        element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/main/section[1]/section/div/div[2]/div[1]/h3'))
        )
    except Exception as e:
        print(f"No se pudo encontrar el elemento: {e}")
        driver.quit()
        return None

    # Obtiene el texto que contiene la cantidad de likes
    likes_text = element.text

    driver.quit()
    return likes_text

#Metodo para obtener los suscriptores de youtube
def obtener_cantidad_suscriptores_youtube(url):
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

#Metodo para obtener los seguidores de twitter
def obtener_seguidores_twitter(url):
    print("Selenium")
    options = Options()
    options.add_argument('--headless') 
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    # Espera hasta que el elemento que contiene la información de likes sea visible
    try:
        element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span"))
        )
    except Exception as e:
        print("No existe red social twitter")
        driver.quit()
        return None

    # Obtiene el texto que contiene la cantidad de likes
    likes_text = element.text

    driver.quit()
    return likes_text


#Metodo para obtener los likes de facebook
def obtener_likes_facebook(url):
    print("Selenium")
    options = Options()
    options.add_argument('--headless') 
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    # Espera hasta que el elemento que contiene la información de likes sea visible
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a[1]"))
        )
    except Exception as e:
        print(f"No se pudo encontrar el elemento: {e}")
        driver.quit()
        return None

    # Obtiene el texto que contiene la cantidad de likes
    likes_text = element.text

    driver.quit()
    return likes_text

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
        data_response = []
        elementos_redes_sociales = driver.find_elements(By.XPATH, "//a[contains(@href, 'facebook.com') or contains(@href, 'twitter.com') or contains(@href, 'youtube.com') or contains(@href, 'linkedin.com') or contains(@href, 'instagram.com')]")

        for elemento in elementos_redes_sociales:
            redes_sociales.append(elemento.get_attribute("href"))
            #print("La red social es: ",redes_sociales[len(redes_sociales)-1])
            social_red = str(redes_sociales[len(redes_sociales)-1])
            if pattern_facebook.match(social_red):
                likes = obtener_likes_facebook(redes_sociales[len(redes_sociales)-1])
                data_response.append("Red Social: ")
                data_response.append(redes_sociales[len(redes_sociales)-1])
                data_response.append("Likes: ")
                data_response.append(likes)
                print("Los likes son: ",likes)
            elif pattern_twitter.match(social_red):
                seguidores = obtener_seguidores_twitter(redes_sociales[len(redes_sociales)-1])
                data_response.append("Red Social: ")
                data_response.append(redes_sociales[len(redes_sociales)-1])
                data_response.append("Seguidores: ")
                data_response.append(seguidores)
                print("Los seguidores son: ",seguidores)

            elif pattern_youtube.match(social_red) or pattern_youtube_01.match(social_red):
                videos = obtener_cantidad_suscriptores_youtube(redes_sociales[len(redes_sociales)-1])
                data_response.append("Red Social: ")
                data_response.append(redes_sociales[len(redes_sociales)-1])
                data_response.append("Suscriptores: ")
                data_response.append(videos)
                print("Los suscriptores son: ",videos)
            elif pattern_linkedin.match(social_red):
                seguidores_li = obtener_cantidad_seguidores_linkedin(redes_sociales[len(redes_sociales)-1])
                data_response.append("Red Social: ")
                data_response.append(redes_sociales[len(redes_sociales)-1])
                data_response.append("Seguidores :")
                data_response.append(seguidores_li)
                print("Los seguidores son: ",seguidores)
            


        driver.quit()
        return data_response

    except Exception as e:
        print("Error al obtener las redes sociales con Selenium")
        #print(e)
        return []

def enviar_a_redis_rsmq(informacion):
    '''data = {"data": informacion}
    response = requests.post(node_url, json=data)'''
    queue_name = 'proyecto'

    # Enviar mensaje a la cola
    redis_connection.lpush(queue_name, json.dumps(informacion))
    data = {"data": informacion}
    response = requests.post(node_url, json=data)
    #print(response.text)
    #redis_client = redis.StrictRedis(host='172.17.0.2', port=6379, decode_responses=True)

    #redis_client.set("mi_clave", informacion)
    #print("Información almacenada directamente en Redis.")




@app.route('/data_web', methods=['POST'])
def data_web():
    data = request.get_json()
    url = data['url']
    redes_sociales_selenium = obtener_redes_sociales_selenium(url)
    print("Redes sociales (Selenium):", redes_sociales_selenium)
    # Enviar la información a Redis RSMQ
    informacion = "\n".join(redes_sociales_selenium)
    enviar_a_redis_rsmq(informacion)
    #return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    respuesta_python = redis_connection.brpop('proyecto', timeout=60)
    if respuesta_python:
        respuesta_python = json.loads(respuesta_python[1])
        print('Respuesta de Node.js:', respuesta_python)
    else:
        print('No hay respuesta de Node.js')

    return json.dumps({'success': True, 'respuesta_python': respuesta_python}), 200, {'ContentType': 'application/json'}



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

'''
#url_pagina = "https://www.coca-cola.com/es/es/"
url_pagina = "https://www.nike.com/es/"
redes_sociales_selenium = obtener_redes_sociales_selenium(url_pagina)
print("Redes sociales (Selenium):", redes_sociales_selenium)
 # Enviar la información a Redis RSMQ
informacion = "\n".join(redes_sociales_selenium)
enviar_a_redis_rsmq(informacion)'''
'''
url_pagina = "https://www.bayer.com/"
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
enviar_a_redis_rsmq(informacion)'''

