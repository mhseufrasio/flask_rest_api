import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..schemas import StoreSchema

blp = Blueprint("stores",__name__, description="Operações com Stores")
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Loja não encontrada.")

    def delete(selfself, store_id):
        try:
            del stores[store_id]
            return {"message":"Loja excluída."}
        except KeyError:
            abort(404, message="Loja não encontrada.")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return {"Lojas":list(stores.value())}

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        for loja in stores.values():
            if store_data["nome"] == loja["nome"]:
                abort(400, message="Loja já existe.")
        store_id = uuid.uuid4().hex
        loja = {**store_data, "id": store_id}
        stores[store_id] = loja
        return loja