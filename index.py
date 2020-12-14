import datetime
from pymongo import MongoClient
from bottle import run, template, get, post, request
import os
import json

MONGO_URL = os.getenv('MONGO_URL')
cliente = MongoClient('mongodb://localhost:27017' if MONGO_URL == "" else MONGO_URL)
metrica = cliente.metrica_database
metricasdb = metrica.metrica_collection

@post('/metrics')
def index():
    body = request.body.read()
    jsonObj = json.loads(body)

    nova_metrica = {
        "umidade": jsonObj["umidade"],
        "temperatura": jsonObj["temperatura"]
    }

    metricasdb.insert_one(nova_metrica)

    return "sucesso"


@get('/metrics')
def lista():
    itens = "<ul>"
    
    for x in metricasdb.find():
        itens += "<li>Umidade: " + str(x['umidade']) + " | Temperatura: " + str(x['temperatura']) + "</li>"
     
    itens += "</ul>"

    return itens

run(host='localhost', port=8083)