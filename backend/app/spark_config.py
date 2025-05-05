from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

def get_spark_context():
    conf = SparkConf() \
        .setAppName("RecipeRecommendationsAPI") \
        .setMaster("spark://spark-master:7077") \
        .set("spark.driver.host", "recipe-app-backend-1") \
        .set("spark.executor.memory", "2g") \
        .set("spark.driver.memory", "2g") \
        .set("spark.cores.max", "4")
    
    sc = SparkContext(conf=conf)
    return sc

def get_spark_session():
    spark = SparkSession.builder \
        .appName("RecipeRecommendationsAPI") \
        .master("spark://spark-master:7077") \
        .config("spark.driver.host", "recipe-app-backend-1") \
        .config("spark.executor.memory", "2g") \
        .config("spark.driver.memory", "2g") \
        .config("spark.cores.max", "4") \
        .getOrCreate()
    return spark 