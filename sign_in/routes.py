from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt
)
from redis import Redis
from dal import get_user_by_email, create_user
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)
redis_client = Redis.from_url("redis://cache:6379/0")

# Inscription
@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    if get_user_by_email(data['email']):
        return jsonify({"message": "Email already exists"}), 400

    if create_user(data['email'], data['password']):
        return jsonify({"message": "User registered successfully"}), 201
    return jsonify({"message": "Registration failed"}), 500

# Connexion
@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    user = get_user_by_email(data['email'])

    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.email)
        return jsonify({"access_token": access_token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Déconnexion
@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]
        redis_client.set(jti, 'revoked', ex=3600)  # Mark the token as revoked in Redis
        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
