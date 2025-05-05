from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
import datetime
from flask_cors import cross_origin

auth_bp = Blueprint('auth', __name__)

# MongoDB
client = MongoClient("mongodb://mongo:27017")  # or localhost for non-docker
db = client["forkast"]
users = db["users"]

@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def register():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({"error": "Email and password are required"}), 400
            
        if users.find_one({"email": data["email"]}):
            return jsonify({"error": "User already exists"}), 409
            
        users.insert_one(data)
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({"error": "Email and password are required"}), 400
            
        user = users.find_one({"email": data["email"], "password": data["password"]})
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401
            
        token = create_access_token(identity=data["email"], expires_delta=datetime.timedelta(days=1))
        return jsonify({"token": token})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
