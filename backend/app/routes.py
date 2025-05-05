from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, udf
from pyspark.sql.types import FloatType
import json
from datetime import datetime
import os
from flask_cors import CORS

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

@main.route("/upload-groceries", methods=["POST", "OPTIONS"])
def upload_groceries():
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        return response

    data = request.get_json()
    if not data:
        return jsonify({"error": "No input received"}), 400
    
    try:
        # Read the latest recipes file from HDFS
        files = spark.sparkContext.wholeTextFiles("hdfs://namenode:9000/data/mysql_recipes_*").keys().collect()
        if not files:
            return jsonify({"error": "No recipe data found"}), 404
        
        latest_file = max(files)
        recipes_df = spark.read.json(latest_file)
        
        # Convert ingredients to lowercase for case-insensitive matching
        user_ingredients = [i.lower() for i in data["ingredients"]]
        
        # Define a UDF to calculate recipe score based on ingredient matches
        def calculate_score(recipe_ingredients):
            try:
                recipe_ingredients = json.loads(recipe_ingredients)
                recipe_ingredients = [i.lower() for i in recipe_ingredients]
                matches = sum(1 for i in user_ingredients if any(i in r for r in recipe_ingredients))
                return float(matches) / len(user_ingredients)
            except:
                return 0.0
        
        score_udf = udf(calculate_score, FloatType())
        
        # Calculate scores and get top 5 recommendations
        recommendations = recipes_df.withColumn(
            "score",
            score_udf(col("ingredients"))
        ).orderBy(col("score").desc()).limit(5)
        
        # Convert to JSON response
        result = recommendations.select(
            col("id").alias("recipe_id"),
            col("title").alias("recipe_title"),
            col("ingredients"),
            col("directions").alias("instructions"),
            col("score")
        ).toJSON().collect()
        
        response = jsonify({
            "recommendations": [json.loads(r) for r in result]
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
