import os
import secrets

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
import models

from resource.item  import blp as itemBlueprint
from resource.store  import blp as storeBlueprint
from resource.tags import blp as tagBlueprint
from resource.user import blp as userBlueprint
from blocklist import BLOCKLIST

def create_app(db_url=None):

    app = Flask(__name__)

    app.config["API_TITLE"] = "Store REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    api =Api(app)

    app.config["JWT_SECRET_KEY"] = "34486445659477776565312485277348265577"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {"description":"The token has been revoked.","error":"token_revoked"}
            ), 
            401
        )
    
    @jwt.needs_fresh_token_loader
    def token__not_fresh_callback(jwt_header, jwt_payload):
        return(
              jsonify(
                {"description":"The token is not refresh.","error":"fresh_token_required"}
            ), 
            401
        )

    @jwt.additional_claims_loader
    def  add_claims_to_jwt(identity):
         if identity == 1:
             return{"is_admin":True}
         return {"is_admin":True}
             


    with app.app_context():
        db.create_all()

    api.register_blueprint(itemBlueprint)
    api.register_blueprint(storeBlueprint)
    api.register_blueprint(tagBlueprint)
    api.register_blueprint(userBlueprint)

    return app

