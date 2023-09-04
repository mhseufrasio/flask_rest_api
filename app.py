import uuid
from flask_smorest import abort
from flask import Flask, request
from db import itens, stores

app = Flask(__name__)



@app.get("/store")
def get_stores():
    return {"stores":list(stores.values())}

@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "nome" not in store_data:
        abort(400,message="O nome da Loja deve ser informado.")
    for loja in stores.values():
        if loja["nome"] == store_data["nome"]:
            abort(400,message="Este nome já está sendo usado ou a Loja já foi cadastrada.")
    store_id = uuid.uuid4().hex
    store = {**store_data, "id":store_id}
    stores[store_id] = store
    return store, 201

@app.post("/item")
def create_item(store_id):
    item_data = request.get_json()
    if("preço" not in item_data
            or "nome" not in item_data
            or "store_id" not in item_data):
        abort(400, message="Algum parâmetro está errado ou faltando.")
    for item in itens.values():
            if item_data["nome"] == item["nome"] and item["store_id"] == item_data["store_id"]:
                abort(400,message="Este item já existe.")
    if item_data["store_id"] not in stores:
        abort(404, message="Loja não encontrada.")
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    itens[item_id] = item
    return item, 201

@app.get("/item")
def get_itens():
    return {"itens":list(itens.values())}

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Loja não encontrada.")

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return itens[item_id]
    except KeyError:
        abort(404, message="Item não encontrado.")

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del itens[item_id]
        return {"message":"Item deletado."}
    except KeyError:
        abort(404,message="Item não encontrado.")

@app.put("/item/<string:item_id>")
def edit_item(item_id):
    item_data = request.get_json()
    if "preço" not in item_data or "name" not in item_data:
        abort(400,message="Confira os parâmetros.")
    try:
        item = itens[item_id]
        item|=item_data
        return item
    except KeyError:
        abort(404,message="Item não encontrado.")

@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message":"Exclusão feita com sucesso."}
    except KeyError:
        abort(404,message="Loja não encontrada.")