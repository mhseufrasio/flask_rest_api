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
    store_id = uuid.uuid4().hex
    store = {**store_data, "id":store_id}
    stores[store_id] = store
    return store, 201

@app.post("/item")
def create_item(store_id):
    item_data = request.get_json()
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