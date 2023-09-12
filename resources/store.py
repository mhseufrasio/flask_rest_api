import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import StoreModel

blp = Blueprint("stores",__name__, description="Operações com Stores")
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = not StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        #não implementado
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"Loja deletada."}, 200

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        loja = StoreModel(**store_data)
        try:
            db.session.add(loja)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Uma Loja com este nome já existe.")
        except SQLAlchemyError:
            abort(500, message="Erro ao cadastrar a Loja.")
        return loja