from flask import Blueprint, request, jsonify
from .services import create_user, authenticate_user

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "User module working"})


@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Basic validation
    if not data or not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"message": "All fields are required"}), 400

    user = create_user(
        name=data["name"],
        email=data["email"],
        password=data["password"]
    )

    if not user:
        return jsonify({"message": "Email already exists"}), 409

    return jsonify({
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }), 201


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password required"}), 400

    user = authenticate_user(
        email=data["email"],
        password=data["password"]
    )

    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }), 200
