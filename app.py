from flask import Flask
from flask_restful import Api
from user.model import UserRegister


app = Flask(__name__)
api = Api(app)


api.add_resource(UserRegister, "/user/register")


if __name__ == "__main__":
    app.run(debug=True)
