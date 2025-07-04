from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token,create_refresh_token, get_jwt, jwt_required
from blocklist import BLOCKLIST

from db import db

from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "users", description="Opetrations on Users")

 
@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).filter():
            abort(409, message="A user with that username already exist.")
        user= UserModel(
            username= user_data["username"],
            password= pbkdf2_sha256.hash(user_data["password"])
        )

        db.session.add(user)
        db.session.commit()

        return{"message":"User created sucessfully."}, 201
    
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        
        if user and  pbkdf2_sha256.verify(user_data["password"], user.passworf):
            access_tokem = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_tokem, "refresh_token":refresh_token}
        
        abort(401, message="Invalid credentials.")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add("jti")
        return{"access_token":new_token}




@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post():
        jti =get_jwt()["jti"]
        BLOCKLIST.ADD(jti)
        return{"message": "Successfully logged out"}

@blp.route("/route/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200
        



 