import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import itens
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Itens", __name__, description="Operações com Itens")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return itens[item_id]
        except KeyError:
            abort(404, message="Item não encontrado.")
    def delete(self, item_id):
        try:
            del itens[item_id]
            return {"message":"Item deletado."}
        except KeyError:
            abort(404, message="Item não encontrado.")
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = itens[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item não encontrado.")

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return {"itens":list(itens.values())}
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        for item in itens.values():
            if item_data["nome"] == item["nome"] and item_data["store_id"] == item["store_id"]:
                abort(400, message="Item já cadastrado.")
        item_id = uuid.uuid4().hex
        item = {**item_data, "item_id":item_id}
        itens[item_id] = item
        return item