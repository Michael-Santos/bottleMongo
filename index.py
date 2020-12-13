import datetime
from pymongo import MongoClient
from bottle import run, template, get

def connect_database():
    a = None
    try:
        a = MongoClient('mongodb://172.17.0.4:27017/')
    except Exception as ex:
        print(ex)
    return a

cliente = connect_database()
banco = cliente.test_database
pessoasdb = banco.test_collection

@get('/save/<name>')
def index(name):
    
    data = datetime.datetime.now()
    pessoa = {
        "nome": name,
        "salvo_em": data
    }

    pessoasdb.insert_one(pessoa)

    return template('<b>{{name}} foi salvo em {{data}}</b>', name=name, data=data)


@get('/')
def lista():
    itens = "<ul>"
    
    for x in pessoasdb.find():
        itens += "<li>" + x['nome'] + " | salvo em: " + str(x['salvo_em']) + "</li>"
     
    itens += "</ul>"

    return itens

run(host='localhost', port=8083)