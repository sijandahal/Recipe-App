from pyspark.sql import SparkSession
from pyspark.sql.functions import col, monotonically_increasing_id
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, DoubleType
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import json
import logging

# Set up minimal logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Spark session
spark = SparkSession.builder \
    .appName("RecipeRecommendations") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .getOrCreate()

# Schema for recipe JSON data
recipe_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("title", StringType(), True),
    StructField("ingredients", StringType(), True),
    StructField("directions", StringType(), True),
    StructField("link", StringType(), True),
    StructField("source", StringType(), True),
    StructField("NER", StringType(), True)
])

# Output schema for recommendations
output_schema = StructType([
    StructField("recipe_id", LongType(), True),
    StructField("recipe_name", StringType(), True),
    StructField("ingredients", StringType(), True),
    StructField("similarity_score", DoubleType(), True)
])

def read_latest_hdfs_file(pattern):
    files = spark.sparkContext.wholeTextFiles(f"hdfs://namenode:9000/data/{pattern}*").collect()
    latest_file = max(files, key=lambda x: x[0])
    parsed_data = json.loads(latest_file[1])
    return spark.createDataFrame(parsed_data)

def read_user_input_file():
    file = spark.sparkContext.wholeTextFiles("hdfs://namenode:9000/data/user_input.json").collect()
    content = json.loads(file[0][1])
    return content

def process_ingredients(ingredients_str):
    try:
        if isinstance(ingredients_str, str):
            try:
                ingredients = json.loads(ingredients_str)
            except:
                ingredients = [ingredients_str]
        else:
            ingredients = ingredients_str
        return ' '.join([str(i).lower().strip() for i in ingredients])
    except:
        return str(ingredients_str).lower().strip()

def calculate_tfidf_similarity(user_ingredients, recipe_ingredients):
    try:
        if not user_ingredients or not recipe_ingredients:
            return 0.0
        vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([user_ingredients, recipe_ingredients])
        return float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
    except:
        return 0.0

def main():
    try:
        recipes_df = read_latest_hdfs_file("mysql_recipes_")
        user_input = read_user_input_file()
        user_ingredients = process_ingredients(user_input.get("ingredients", ""))

        recipes_df = recipes_df.withColumn("row_id", monotonically_increasing_id())
        total_recipes = recipes_df.count()
        batch_size = 100
        scored = []

        for i in range(0, total_recipes, batch_size):
            batch = recipes_df.filter((col("row_id") >= i) & (col("row_id") < i + batch_size)).collect()
            for row in batch:
                recipe_ingredients = process_ingredients(row["ingredients"])
                score = calculate_tfidf_similarity(user_ingredients, recipe_ingredients)
                scored.append({
                    "recipe_id": row["id"],
                    "recipe_name": row["title"],
                    "ingredients": row["ingredients"],
                    "similarity_score": score
                })

        top = sorted(scored, key=lambda x: x["similarity_score"], reverse=True)[:5]
        logger.info(f"Top recommendations data: {json.dumps(top, indent=2)}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"hdfs://namenode:9000/data/recommendations_{timestamp}.json"
        recommendations_df = spark.createDataFrame(top, schema=output_schema)
        recommendations_df.write.mode("overwrite").json(output_path)

    except Exception as e:
        pass
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
