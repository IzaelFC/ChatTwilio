import pandas as pd


dados = pd.read_json("https://economia.awesomeapi.com.br/json/last/USD-BRL")
dados = dados.transpose()
dolar = dados['ask'][0]
#print(dolar)

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
        dados = dados.transpose()
        dolar = dados['ask'][0]
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


    if not responded:
        msg.body('Comando desconhecido!\n\nDigite 1 para ver o valor do dolar.\nDigite 2 para ver a temperatura do dia.')
    return str(resp)


if __name__ == '__main__':
   app.run()