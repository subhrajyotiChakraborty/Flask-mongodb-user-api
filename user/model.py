import uuid
from flask import request, jsonify, make_response
from flask_restful import Resource
from db import db


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_dict = request.get_json()
        user = {
            "_id": uuid.uuid4().hex,
            "name": user_dict["name"],
            "email": user_dict["email"],
            "password": user_dict["password"]
        }
        db["users"].insert_one(user)
        del user["password"]
        return make_response(jsonify(user), 201)
