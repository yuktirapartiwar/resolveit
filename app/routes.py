from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import User
from app import db

main = Blueprint("main", __name__)

@main.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    hashed_pw = generate_password_hash(data["password"])

    user = User(
        name = data["name"],
        email = data["email"],
        password_hash = hashed_pw,
        role = data["role"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!!"}), 201


@main.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity = user.id)

    return jsonify({"access_token": access_token}), 200
