from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
import datetime

auth_bp = Blueprint('auth', __name__)

# MongoDB
client = MongoClient("mongodb://mongo:27017")  # or localhost for non-docker
db = client["forkast"]
users = db["users"]

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if users.find_one({"email": data["email"]}):
        return jsonify({"error": "User already exists"}), 409
    users.insert_one(data)
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users.find_one({"email": data["email"], "password": data["password"]})
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    token = create_access_token(identity=data["email"], expires_delta=datetime.timedelta(days=1))
    return jsonify({"token": token})
