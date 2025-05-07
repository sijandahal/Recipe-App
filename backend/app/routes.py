from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, udf
from pyspark.sql.types import FloatType
import json
from datetime import datetime
import os
from flask_cors import CORS
from hdfs import InsecureClient

main = Blueprint("main", __name__)
CORS(main, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

client = MongoClient("mongodb://mongo:27017")  # MongoDB container name
db = client.forkast
collection = db.user_inputs

# Initialize Spark session
spark = SparkSession.builder \
    .appName("RecipeRecommendationsAPI") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "1g") \
    .config("spark.driver.memory", "1g") \
    .config("spark.cores.max", "2") \
    .config("spark.sql.shuffle.partitions", "2") \
    .config("spark.driver.host", "backend") \
    .config("spark.driver.bindAddress", "0.0.0.0") \
    .config("spark.network.timeout", "600s") \
    .config("spark.executor.heartbeatInterval", "60s") \
    .config("spark.driver.extraJavaOptions", "-Djava.net.preferIPv4Stack=true") \
    .config("spark.executor.extraJavaOptions", "-Djava.net.preferIPv4Stack=true") \
    .config("spark.executor.cores", "2") \
    .config("spark.executor.memoryOverhead", "512m") \
    .getOrCreate()

# Define schema for recipes
recipe_schema = {
    "id": "integer",
    "title": "string",
    "ingredients": "string",
    "directions": "string",
    "link": "string",
    "source": "string",
    "NER": "string"
}

hdfs_client = InsecureClient('http://namenode:9870', user='root')
def write_to_hdfs(data, hdfs_path):
    """Write data to HDFS using hdfs.InsecureClient"""
    try:
        # Format data as JSON with proper indentation
        json_str = json.dumps(data, indent=2)
        
        # Create parent directory if it doesn't exist
        parent_dir = os.path.dirname(hdfs_path)
   
        hdfs_client.makedirs(parent_dir)
     
        # Write data to HDFS
        with hdfs_client.write(hdfs_path, overwrite=True, encoding='utf-8') as writer:
            writer.write(json_str)
            
    
        return True
    except Exception as e:
    
        return False
 
def read_from_hdfs(hdfs_path):
    """Read data from HDFS using the hdfs client"""
    try:
        with hdfs_client.read(hdfs_path, encoding='utf-8') as reader:
            data = reader.read()
            return json.loads(data)
    except Exception as e:
      
        return None
 
@main.route("/upload-groceries", methods=["POST", "OPTIONS"])
def upload_groceries():
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        return response
 
    try:
        data = request.json
        if not data or "ingredients" not in data:
            return jsonify({"error": "No ingredients provided"}), 400
 
        # Extract just the ingredients and add timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ingredients_data = {
            "ingredients": data["ingredients"],
            "timestamp": timestamp
        }

        
        # Write data to HDFS with timestamp in filename
        hdfs_path = '/data/user_input.json'
        if not write_to_hdfs(ingredients_data, hdfs_path):
            return jsonify({"error": "Failed to write to HDFS"}), 500
            
    
        return jsonify({"message": "Ingredients uploaded successfully"}), 200
 
    except Exception as e:
       
        return jsonify({"error": str(e)}), 500
 
@main.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        return jsonify({
            "status": "healthy",
            "message": "Service is running"
        }), 200
    except Exception as e:
        
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500
 
@main.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    try:
        # Get ingredients from request
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        
        if not ingredients:
            return jsonify({"error": "No ingredients provided"}), 400
        
        # Write ingredients to HDFS
        with hdfs_client.write('/data/user_input.json', encoding='utf-8') as writer:
            json.dump(data, writer)
        
        # Execute Spark job
        spark_script = '/app/spark-scripts/recommendations.py'
        result = subprocess.run(['python3', spark_script],
                              capture_output=True,
                              text=True)
        
        if result.returncode != 0:
            
            return jsonify({"error": "Failed to generate recommendations"}), 500
        
        # Read recommendations from HDFS
        try:
            with hdfs_client.read('/data/recommendations.json') as reader:
                recommendations = json.load(reader)
            return jsonify(recommendations)
        except Exception as e:
            
            return jsonify({"error": "Failed to read recommendations"}), 500
        
    except Exception as e:
        
        return jsonify({"error": str(e)}), 500
 

import re
@main.route('/api/latest-recommendations', methods=['GET'])
def latest_recommendations():
    try:
        # Identify the latest file (assuming sorted naming with timestamps)
        files = hdfs_client.list("/data")
        latest_file = sorted(
            [f for f in files if f.startswith("recommendations_") and f.endswith(".json")],
            reverse=True
        )[0]

        # Read the file line-by-line and parse each JSON object
        with hdfs_client.read(f"/data/{latest_file}", encoding="utf-8") as reader:
            lines = reader.read().splitlines()
            data = [json.loads(line) for line in lines if line.strip()]

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Failed to read latest recommendations: {str(e)}"}), 500
