from flask import Blueprint, request, jsonify
from pymongo import MongoClient

main = Blueprint("main", __name__)

client = MongoClient("mongodb://mongo:27017")  # MongoDB container name
db = client.forkast
collection = db.user_inputs

@main.route("/upload-groceries", methods=["POST"])
def upload_groceries():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input received"}), 400
    inserted = collection.insert_one(data)
    return jsonify({"message": "Data stored", "id": str(inserted.inserted_id)})
