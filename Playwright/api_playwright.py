import time
import asyncio
import requests,json
from playwright.async_api import async_playwright
import re
from flask import Flask, request, jsonify

node_url = 'http://nodejs_app:6000/data_play'
lista_redes_sociales = []

pattern_facebook = re.compile(r'^https?://(?:www\.)?facebook\.com/[a-zA-Z0-9.]+/?$')
pattern_twitter = re.compile(r'^https?://(?:www\.)?twitter\.com/[a-zA-Z0-9_]+/?$')
pattern_instagram = re.compile(r'^https?://(?:www\.)?instagram\.com/[a-zA-Z0-9_.]+/?$')
pattern_linkedin = re.compile(r'^https?://(?:www\.)?linkedin\.com/company/[a-zA-Z0-9_-]+/?$')
youtube_regex = re.compile(r'https://www\.youtube\.com/[^/]+')

def obtener_url_facebook(lista):
    for url in lista:
        coincidencia = pattern_facebook.match(url)
        if coincidencia:
            url_completa = coincidencia.group(0)
            return url_completa
    return None

def obtener_url_twitter(lista):
    for url in lista:
        coincidencia = pattern_twitter.match(url)
        if coincidencia:
            url_completa = coincidencia.group(0)
            return url_completa
    return None

def obtener_url_linkedin(lista):
    for url in lista:
        coincidencia = pattern_linkedin.match(url)
        if coincidencia:
            url_completa = coincidencia.group(0)
            return url_completa
    return None
def obtener_url_youtube(lista):
    # Expresión regular para coincidir con URLs de YouTube

    for url in lista:
        coincidencia = youtube_regex.search(url)
        if coincidencia:
            url_completa = coincidencia.group(0)
            return url_completa
    return None

async def obtener_likes_con_xpath(url, xpath):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)

        # Agregar tiempo de espera para que la página cargue completamente
        await page.wait_for_selector(f'xpath={xpath}')

        # Obtener el texto que contiene la información de "Me gusta" utilizando XPath
        likes_text = await page.inner_text(f'xpath={xpath}')

        # Imprimir la cantidad de "Me gusta"
        #print("subs YT", likes_text)
        await browser.close()
    return likes_text

async def obtener_redes_sociales_playwright(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)

        redes_sociales = await page.query_selector_all("a[href*='facebook.com'], a[href*='twitter.com'], a[href*='instagram.com'], a[href*='youtube.com'], a[href*='linkedin.com']")

        resultados = [await red_social.get_attribute("href") for red_social in redes_sociales]

        await browser.close()

    return resultados

async def init(url):
    data_play = []
    url_pagina = url
    redes_sociales_playwright = await obtener_redes_sociales_playwright(url_pagina)
    lista_redes_sociales = redes_sociales_playwright.copy()
    #Obtener toda la informacion desde facebook
    url_facebook = obtener_url_facebook(lista_redes_sociales)
    if url_facebook is None:
        data_play.append("Esta empresa no tiene pagina de facebook")
        print("Esta empresa no tiene pagina de facebook")
    else:
        xpath_ejemplo = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a[1]"
        resultado = await obtener_likes_con_xpath(url_facebook, xpath_ejemplo)
        print("seguidores facebook", resultado)
        data_play.append("Seguidores de facebook: ")
        data_play.append(resultado)

    #obtener toda la informacion desde twitter
    url_twitter = obtener_url_twitter(lista_redes_sociales)
    if url_twitter is None:
        data_play.append("Esta empresa no tiene pagina de twitter")
        print("Esta empresa no tiene pagina de twitter")
    else:
        xpath_ejemplo = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span'
        resultado = await obtener_likes_con_xpath(url_twitter, xpath_ejemplo)
        print("seguidores twitter", resultado)
        data_play.append("Seguidores de twitter: ")
        data_play.append(resultado)


    #obtener toda la informacion desde youtube
    url_youtube = obtener_url_youtube(lista_redes_sociales)
    if url_youtube is None:
        print("Esta empresa no tiene canal de youtube")
        data_play.append("Esta empresa no tiene canal de youtube")
    else:
        xpath_ejemplo = '//*[@id="subscriber-count"]'
        resultado = await obtener_likes_con_xpath(url_youtube, xpath_ejemplo)
        print("subs YT", resultado)
        data_play.append("Suscriptores en YT: ")
        data_play.append(resultado)

    #obtener toda la informacion desde linkedin
    url_linkedin = obtener_url_linkedin(lista_redes_sociales)
    if url_linkedin is None:
        print("Esta empresa no tiene pagina de linkedin")
        data_play.append("Esta empresa no tiene pagina de linkedin")
    else:
        xpath_ejemplo = '/html/body/main/section[1]/section/div/div[2]/div[1]/h3'
        resultado = await obtener_likes_con_xpath(url_linkedin, xpath_ejemplo)
        print("seguidores likedin", resultado) 
        data_play.append("Seguidores de linkedin: ")
        data_play.append(resultado)


    return data_play

def enviar_a_redis_rsmq(informacion):
    data = {"data": informacion}
    response = requests.post(node_url, json=data)

app = Flask(__name__)


@app.route('/data_web', methods=['POST'])
def data_web():
    data = request.get_json()
    url = data['url']
    informacion = asyncio.run(init(url))
    
    # Enviar la información a Redis RSMQ
    informacion = "\n".join(informacion)
    enviar_a_redis_rsmq(informacion)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5050)