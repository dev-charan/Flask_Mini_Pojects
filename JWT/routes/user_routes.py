from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from model import db, User
from werkzeug.security import generate_password_hash, check_password_hash

user = Blueprint('user', __name__)

@user.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Welcome {current_user}!"}), 200

@user.route("/me", methods=["GET"])
@jwt_required()
def get_user():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    return jsonify({"username": user.username}), 200

@user.route("/update-password", methods=["POST"])
@jwt_required()
def update_password():
    data = request.get_json()
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if not check_password_hash(user.password, data["old_password"]):
        return jsonify({"message": "Old password incorrect"}), 400

    user.password = generate_password_hash(data["new_password"])
    db.session.commit()
    return jsonify({"message": "Password updated"}), 200

@user.route("/delete-account", methods=["DELETE"])
@jwt_required()
def delete_account():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200
