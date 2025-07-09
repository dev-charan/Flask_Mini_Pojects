from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, get_jwt
)
from model import db, User
from utils.token_blocklist import add_token_to_blocklist

auth = Blueprint('auth', __name__)

@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(
        username=data["username"]).first():
        return jsonify({"message": "User already exists"}),
    409

    hashed = generate_password_hash(data["password"])
    new_user = User(username=data["username"], password=hashed)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registered successfully"}), 201

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user and check_password_hash(user.password, data["password"]):
        access = create_access_token(identity=user.username)
        refresh = create_refresh_token(identity=user.username)
        return jsonify(access_token=access, refresh_token=refresh), 200
    return jsonify({"message": "Invalid credentials"}), 401

@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200

@auth.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    add_token_to_blocklist(jti)
    return jsonify({"message": "Token revoked"}), 200
