from pyspark.sql import SparkSession
from pyspark.sql.functions import col, monotonically_increasing_id
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, DoubleType
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Spark session
spark = SparkSession.builder \
    .appName("RecipeRecommendations") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .getOrCreate()

# Input recipe schema
recipe_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("title", StringType(), True),
    StructField("ingredients", StringType(), True),
    StructField("directions", StringType(), True),
    StructField("link", StringType(), True),
    StructField("source", StringType(), True),
    StructField("NER", StringType(), True)
])

# Output schema
output_schema = StructType([
    StructField("recipe_id", LongType(), True),
    StructField("recipe_name", StringType(), True),
    StructField("ingredients", StringType(), True),
    StructField("similarity_score", DoubleType(), True)
])

def read_latest_hdfs_file(pattern):
    files = spark.sparkContext.wholeTextFiles(f"hdfs://namenode:9000/data/{pattern}*").collect()
    if not files:
        raise RuntimeError(f"No files found matching pattern: {pattern}")
    latest_file = max(files, key=lambda x: x[0])
    parsed_data = json.loads(latest_file[1])
    return spark.createDataFrame(parsed_data)

def read_user_input_file():
    file = spark.sparkContext.wholeTextFiles("hdfs://namenode:9000/data/user_input.json").collect()
    if not file:
        raise RuntimeError("user_input.json not found.")
    return json.loads(file[0][1])

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

# 🔧 Key Fix: Move part file to flat .json using HDFS Java API
def move_part_file_to_flat_json(tmp_path, final_path):
    from py4j.java_gateway import java_import

    hadoop_conf = spark._jsc.hadoopConfiguration()
    hadoop_conf.set("fs.defaultFS", "hdfs://namenode:9000")  # 🔥 Important fix

    java_import(spark._jvm, "org.apache.hadoop.fs.FileSystem")
    java_import(spark._jvm, "org.apache.hadoop.fs.Path")

    fs = spark._jvm.FileSystem.get(hadoop_conf)
    tmp_dir_path = spark._jvm.Path(tmp_path)
    final_file_path = spark._jvm.Path(final_path)

    file_statuses = fs.listStatus(tmp_dir_path)
    for status in file_statuses:
        name = status.getPath().getName()
        if name.startswith("part-") and name.endswith(".json"):
            part_path = status.getPath()
            fs.rename(part_path, final_file_path)
            fs.delete(tmp_dir_path, True)
            logger.info(f"✅ Moved {name} to {final_path}")
            break

def main():
    try:
        recipes_df = read_latest_hdfs_file("mysql_recipes_")
        user_input = read_user_input_file()
        user_ingredients = process_ingredients(user_input.get("ingredients", ""))

        recipes_df = recipes_df.withColumn("row_id", monotonically_increasing_id())
        total_recipes = recipes_df.count()
        scored = []

        for i in range(0, total_recipes, 100):
            batch = recipes_df.filter((col("row_id") >= i) & (col("row_id") < i + 100)).collect()
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
        print(json.dumps(top, indent=2))

        # Save to HDFS
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tmp_path = f"hdfs://namenode:9000/data/tmp_recommendations_{timestamp}"
        final_path = f"/data/recommendations_{timestamp}.json"

        spark.createDataFrame(top, schema=output_schema) \
            .coalesce(1) \
            .write \
            .mode("overwrite") \
            .option("compression", "none") \
            .json(tmp_path)

        move_part_file_to_flat_json(tmp_path, final_path)

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
