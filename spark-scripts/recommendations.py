from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, array_contains, lit, collect_list, struct, row_number, from_json, to_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType
from pyspark.sql.window import Window
import json
from datetime import datetime

# Initialize Spark session
spark = SparkSession.builder \
    .appName("RecipeRecommendations") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .getOrCreate()

# Define schema for recipes
recipe_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("title", StringType(), True),
    StructField("ingredients", StringType(), True),
    StructField("directions", StringType(), True),
    StructField("link", StringType(), True),
    StructField("source", StringType(), True),
    StructField("NER", StringType(), True)
])

# Define schema for user data
user_schema = StructType([
    StructField("users", ArrayType(
        StructType([
            StructField("_id", StringType(), True),
            StructField("email", StringType(), True),
            StructField("password", StringType(), True)
        ])
    ), True),
    StructField("ratings", ArrayType(
        StructType([
            StructField("user_id", StringType(), True),
            StructField("recipe_id", IntegerType(), True),
            StructField("rating", IntegerType(), True)
        ])
    ), True),
    StructField("comments", ArrayType(
        StructType([
            StructField("user_id", StringType(), True),
            StructField("recipe_id", IntegerType(), True),
            StructField("comment", StringType(), True)
        ])
    ), True)
])

# Read data from HDFS
def read_latest_hdfs_file(pattern, schema=None):
    # Get list of files matching pattern
    files = spark.sparkContext.wholeTextFiles(f"hdfs://namenode:9000/data/{pattern}*").keys().collect()
    if not files:
        raise Exception(f"No files found matching pattern: {pattern}")
    # Get the latest file
    latest_file = max(files)
    return spark.read.schema(schema).json(latest_file)

# Read recipes and user data
recipes_df = read_latest_hdfs_file("mysql_recipes_", recipe_schema)
user_data_df = read_latest_hdfs_file("mongo_data_", user_schema)

# Extract users from nested structure
users_df = user_data_df.select(explode("users").alias("user")).select(
    col("user._id").alias("user_id"),
    col("user.email")
)

# Preprocess recipes data
recipes_df = recipes_df.select(
    col("id").alias("recipe_id"),
    col("title").alias("recipe_title"),
    col("ingredients"),
    col("directions").alias("instructions"),
    col("NER").alias("diet")
)

# Function to calculate recipe score based on ingredients match
def calculate_recipe_score(user_ingredients, recipe_ingredients):
    # For now, assign a random score since we don't have user preferences
    from random import random
    return random()

# Register UDF for score calculation
from pyspark.sql.types import FloatType
from pyspark.sql.functions import udf

calculate_score_udf = udf(calculate_recipe_score, FloatType())

# Generate recommendations
def generate_recommendations(users_df, recipes_df, top_n=5):
    # Cross join users with recipes
    recommendations = users_df.crossJoin(recipes_df)
    
    # Calculate scores (random for now)
    recommendations = recommendations.withColumn(
        "score",
        calculate_score_udf(lit(None), lit(None))
    )
    
    # Rank recipes for each user
    window = Window.partitionBy("user_id").orderBy(col("score").desc())
    recommendations = recommendations.withColumn("rank", row_number().over(window))
    
    # Get top N recommendations
    top_recommendations = recommendations.filter(col("rank") <= top_n)
    
    # Format output
    output = top_recommendations.groupBy("user_id", "email").agg(
        collect_list(
            struct(
                col("recipe_id"),
                col("recipe_title"),
                col("score")
            )
        ).alias("recommendations")
    )
    
    return output

# Generate recommendations
recommendations_df = generate_recommendations(users_df, recipes_df)

# Convert recommendations to JSON format
recommendations_json = recommendations_df.select(
    col("user_id"),
    col("email"),
    to_json(col("recommendations")).alias("recommendations")
).toPandas().to_json(orient="records")

# Write recommendations to HDFS
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f"hdfs://namenode:9000/data/recommendations_{timestamp}.json"

# Write JSON string to HDFS
spark.sparkContext.parallelize([recommendations_json]).saveAsTextFile(output_path)

# Stop Spark session
spark.stop() 