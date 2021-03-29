import uuid
from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_expects_json import expects_json
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import bcrypt
from db import db
from user.schema import user_register, user_login


class UserRegister(Resource):
    @classmethod
    @expects_json(user_register)
    def post(cls):
        user_dict = request.get_json()

        is_user_present = db["users"].find_one({
            "email": user_dict["email"]
        })
        if is_user_present:
            return make_response({"error": "User already registered"}, 400)
        else:
            access_token = create_access_token(identity=user_dict["email"])
            user = {
                "_id": uuid.uuid4().hex,
                "name": user_dict["name"],
                "email": user_dict["email"],
                "password": user_dict["password"],
                "token": access_token
            }
            hashed = bcrypt.hashpw(user_dict['password'].encode("utf-8"), bcrypt.gensalt())
            user["password"] = hashed
            db["users"].insert_one(user)
            del user["password"]
            return make_response(jsonify(user), 201)


class UserLogin(Resource):
    @classmethod
    @expects_json(user_login)
    def post(cls):
        user_login_dict = request.get_json()
        user = db["users"].find_one({
            "email": user_login_dict["email"]
        })
        if user and bcrypt.checkpw(user_login_dict['password'].encode("utf-8"), user["password"]):
            access_toke = create_access_token(identity=user["email"])
            user["token"] = access_toke
            db["users"].update_one({"email": user["email"]}, {"$set": {"token": access_toke}})
            del user["password"]
            return make_response({"user": user}, 200)
        elif user and not bcrypt.checkpw(user_login_dict['password'].encode("utf-8"), user["password"]):
            return make_response({"error": "Wrong credentials"}, 400)
        else:
            return make_response({"error": "User not registered, please register"}, 400)


class GetUser(Resource):
    @classmethod
    @jwt_required()
    def get(cls, user_id):
        current_user_email = get_jwt_identity()
        user = db["users"].find_one({
            "email": current_user_email
        })
        if user:
            del user["password"]
            return make_response({"user": user}, 200)
        return make_response({"error": f"Unable to find the user with id {user_id}"}, 400)
