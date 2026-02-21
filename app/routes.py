from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User, Ticket
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


@main.route("/tickets", methods=["POST"])
@jwt_required()
def create_ticket():
    data = request.get_json()
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if user.role != "EMPLOYEE":
        return jsonify({"error": "Only employees can create tickets"}), 403

    ticket = Ticket(
        title = data["title"],
        description = data["description"],
        created_by = user.id
    )

    db.session.add(ticket)
    db.session.commit()

    return jsonify({"message": "Ticket created", "ticket_id": ticket.id}), 201
