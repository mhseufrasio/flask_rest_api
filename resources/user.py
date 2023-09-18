import os

import requests
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, create_refresh_token, get_jwt_identity

from db import db
from models import UserModel
from schemas import UserSchema, UserRegisterSchema
from blocklist import BLOCKLIST

blp = Blueprint("Users", __name__, description="Operações com usuarios")


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "Usuário excluído."}, 200


def send_simple_message(to, subject, body):
    domain = os.getenv("MAILGUN_API_KEY")
    return requests.post(f"https://api.mailgun.net/v3/{domain}/messages", auth=("api", os.getenv("MAILGUN_API_KEY")),
                         data={"from": f"Your name <mailgun@{domain}>", "to":[to], "subject": subject, "text": body})


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="Este User já existe.")

        user = UserModel(username=user_data["username"], password=pbkdf2_sha256.hash((user_data["password"])), email=user_data["email"])
        db.session.add(user)
        db.session.commit()

        send_simple_message(to=user.email, subject="Inscrição feita com sucesso.", body=f"Hi {user.username}! You have sucessfully signed to the REST API.")

        return {"message": "Usuário criado com sucesso."}


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            acess_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"acess_token": acess_token, "refresh_token":refresh_token}, 200
        abort(401, message="Usuário ou senha incorreto.")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Acesso encerrado."}, 200


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token":new_token}, 200