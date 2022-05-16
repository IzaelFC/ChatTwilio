import pandas as pd
from googletrans import Translator
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False


    if '1' in incoming_msg:
        #Retorna o valor do dolar 
        dados = pd.read_json("https://economia.awesomeapi.com.br/json/last/USD-BRL")
        dolar = dados['USDBRL']['ask']
        msg.body(f'Valor do dólar: {dolar}')
        responded = True


    if '2' in incoming_msg:
        site = pd.read_json("https://api.hgbrasil.com/weather?woeid=422218")
        cidade = site['results']['city']
        temperatura = site['results']['temp']
        min = site['results']['forecast'][0]['min']
        max = site['results']['forecast'][0]['max']
        descricao = site['results']['forecast'][0]['description']
        msg.body(f'Cidade: {cidade}\nTemperatura: {temperatura} graus.\nDescrição: {descricao}\nMin: {min}\nMax: {max}')
        responded = True
    

    if '3' in incoming_msg:
        site = pd.read_json("https://gnews.io/api/v4/search?q=example&token=d0df6239c6d844dd06030a0be7471059&lang=en")
        dados = pd.DataFrame(site)

        titulo = dados['articles'][0]['title']
        descricao = dados['articles'][0]['description']
        url = dados['articles'][0]['url']

        translator = Translator()

        titulo_traduzido = translator.translate(titulo, dest='pt').text
        descricao_traduzida = translator.translate(descricao, dest='pt').text

        msg.body(f'Título: {titulo_traduzido}\n\nDescrição: {descricao_traduzida}\n\nLink: {url}')
        responded = True


    if '4' in incoming_msg:
        #msg.media("https://picsum.photos/200/300")
        msg.media("https://source.unsplash.com/1240x720/?landscape")
        responded = True


    if '5' in incoming_msg:
        def get_random_page():
            url = 'https://pt.wikipedia.org/w/api.php'
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'random',
                'rnnamespace': 0,
                'rnlimit': 1
            }
            response = requests.get(url, params=params)
            data = response.json()
            title = data['query']['random'][0]['title']
            return title


        def get_page_content(title):
            url = 'https://pt.wikipedia.org/w/api.php'
            params = {
                'action': 'query',
                'format': 'json',
                'prop': 'extracts',
                'exintro': '',
                'explaintext': '',
                'titles': title
            }
            response = requests.get(url, params=params)
            data = response.json()
            page_id = list(data['query']['pages'].keys())[0]
            content = data['query']['pages'][page_id]['extract']
            return content

        tudo = get_page_content(get_random_page())
        msg.body(f'{tudo}')
        responded = True

    
    if '6' in incoming_msg:
        site = pd.read_json("https://positive-vibes-api.herokuapp.com/songs/random")
        nome_artista = site['data']['artist_name']
        nome_musica = site['data']['name']
        musica = site['data']['audio']
        msg.body(f"Nome do artista: {nome_artista}\nNome da música: {nome_musica}") and msg.media(musica)
        responded = True

    
    if '7' in incoming_msg:
        site = requests.get("https://db.ygoprodeck.com/api/v7/randomcard.php").json()

        nome = site["name"]
        tipo = site["type"]
        descrição = site["desc"]
        carta = site["card_images"][0]["image_url"]

        #Tradução
        translator = Translator()
        nome_traduzido = translator.translate(nome, dest='pt').text
        tipo_traduzido = translator.translate(tipo, dest='pt').text
        descrição_traduzido = translator.translate(descrição, dest='pt').text

        msg.body(f'Nome: {nome_traduzido}\nTipo: {tipo_traduzido}\n\nDescrição: {descrição_traduzido}')
        msg.media(carta)
        responded = True

    
    if '8' in incoming_msg:
        site = requests.get("https://v2.jokeapi.dev/joke/Any?explicit-flag").json()
        translator = Translator()

        if site["type"] == "single":
            single_translate = translator.translate(site["joke"], dest='pt').text
            msg.body(f'Inglês:\n\n{site["joke"]}\n\n\nPortuguês:\n\n{single_translate}')
        else:
            setup_translate = translator.translate(site["setup"], src="en", dest="pt").text
            delivery_translate = translator.translate(site["delivery"], src="en", dest="pt").text
            msg.body(f'Inglês:\n\n{site["setup"]}\n{site["delivery"]}\n\n\nPortuguês:\n\n{setup_translate}\n{delivery_translate}')
        responded = True


    if not responded:
        msg.body('Comando desconhecido!\n\nDigite 1 para ver o valor do dolar.\nDigite 2 para ver a temperatura do dia.\nDigite 3 para ver uma noticia.\nDigite 4 para ver uma imagem.\nDigite 5 para ver o conteudo de uma página aleatória do Wikipedia.\nDigite 6 para relaxar com uma musica.\nDigite 7 para ver uma carta aleatória do Yugioh.\nDigite 8 para ver uma piada.')
    return str(resp)


if __name__ == '__main__':
   app.run()