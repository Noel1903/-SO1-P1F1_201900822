import time
import asyncio
import requests,json
from playwright.async_api import async_playwright
from flask import Flask, request, jsonify

node_url = 'http://nodejs_app:6000/data_play'

def urlSearch(pagina,lista):
        for url in lista:
            if url.find(pagina) != -1:
                return url
        return ""

async def obtener_likes_con_xpath(url, xpath):
    print("Buscando en:",url)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_selector(f'xpath={xpath}')
        likes_text = await page.inner_text(f'xpath={xpath}')
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

async def searchFb(links,data_play):
    if urlSearch("facebook",links)=="":
        data_play.append("Esta empresa no tiene pagina de facebook")
        print("Esta empresa no tiene pagina de facebook")
    else:
        xpath_ejemplo = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a[1]"
        resultado = await obtener_likes_con_xpath(urlSearch("facebook",links), xpath_ejemplo)
        print("seguidores facebook", resultado)
        data_play.append(f"Seguidores de facebook: '{resultado}'")

async def searchTw(links,data_play):
    if urlSearch("twitter",links)=="":
        data_play.append("Esta empresa no tiene pagina de twitter")
        print("Esta empresa no tiene pagina de twitter")
    else:
        xpath_ejemplo = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span'
        resultado = await obtener_likes_con_xpath(urlSearch("twitter",links), xpath_ejemplo)
        print("seguidores twitter", resultado)
        data_play.append(f"Seguidores de twitter: '{resultado}'")

async def searchYt(links,data_play):
    if urlSearch("youtube",links)=="":
        print("Esta empresa no tiene canal de youtube")
        data_play.append("Esta empresa no tiene canal de youtube")
    else:
        xpath_ejemplo = '//*[@id="subscriber-count"]'
        resultado = await obtener_likes_con_xpath(urlSearch("youtube",links), xpath_ejemplo)
        print("subs YT", resultado)
        data_play.append(f"Suscriptores en YT: '{resultado}'")

async def searchIn(links,data_play):
    if urlSearch("linkedin",links)=="":
        print("Esta empresa no tiene pagina de linkedin")
        data_play.append("Esta empresa no tiene pagina de linkedin")
    else:
        xpath_ejemplo = '/html/body/main/section[1]/section/div/div[2]/div[1]/h3'
        resultado = await obtener_likes_con_xpath(urlSearch("linkedin",links), xpath_ejemplo)
        print("seguidores likedin", resultado) 
        data_play.append(f"Seguidores de linkedin: '{resultado}'")

async def init(url):
    data_play = []
    url_pagina = url
    links = await obtener_redes_sociales_playwright(url_pagina)
    
    t1=searchFb(links,data_play)
    t2=searchTw(links,data_play)
    await asyncio.gather(t1,t2,searchYt(links,data_play),searchIn(links,data_play))
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
    
    print("\ninformacion: \n",informacion)
    # Enviar la información a Redis RSMQ
    """ informacion = "\n".join(informacion)
    enviar_a_redis_rsmq(informacion) """
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5050)