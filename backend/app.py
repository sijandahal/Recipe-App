from pyspark.sql import SparkSession
import json
from datetime import datetime

# Initialize Spark session for recommendations
spark = SparkSession.builder \
    .appName("RecipeRecommendationsAPI") \
    .getOrCreate()

@app.route('/api/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    try:
        # Read the latest recommendations file
        files = spark.sparkContext.wholeTextFiles("hdfs://namenode:9000/data/recommendations_*").keys().collect()
        if not files:
            return jsonify({"error": "No recommendations found"}), 404
        
        latest_file = max(files)
        recommendations_df = spark.read.json(latest_file)
        
        # Filter for specific user
        user_recommendations = recommendations_df.filter(col("user_id") == user_id)
        
        if user_recommendations.count() == 0:
            return jsonify({"error": "No recommendations found for user"}), 404
        
        # Convert to JSON
        recommendations = user_recommendations.collect()[0].asDict()
        
        return jsonify(recommendations)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500 