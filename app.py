from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_jsonschema_validator import JSONSchemaValidator
from user.model import UserRegister, UserLogin, GetUser



app = Flask(__name__)
api = Api(app)
app.config["JWT_SECRET_KEY"] = "user-api-test-secret"
JSONSchemaValidator(app=app, root="schemas")
jwt = JWTManager(app)


api.add_resource(UserRegister, "/user/register")
api.add_resource(UserLogin, "/user/login")
api.add_resource(GetUser, "/user/<string:user_id>")


if __name__ == "__main__":
    app.run(debug=True)
