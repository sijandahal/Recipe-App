import mysql.connector
import pymongo
from hdfs import InsecureClient
import json
import pandas as pd
from datetime import datetime

# HDFS client setup
hdfs_client = InsecureClient('http://namenode:9870')

# MySQL connection
mysql_conn = mysql.connector.connect(
    host="mysql",
    user="root",
    password="root",
    database="forkast"
)

# MongoDB connection
mongo_client = pymongo.MongoClient("mongodb://mongo:27017/")
mongo_db = mongo_client["forkast"]

def get_mysql_recipes():
    print("📊 Fetching recipes from MySQL...")
    cursor = mysql_conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM recipes")
    recipes = cursor.fetchall()
    cursor.close()
    print(f"✅ Retrieved {len(recipes)} recipes from MySQL")
    return recipes

def get_mongo_data():
    print("📊 Fetching data from MongoDB...")
    # Add collections you want to export
    collections = ["users", "ratings", "comments"]  # Add your MongoDB collections
    mongo_data = {}
    
    for collection_name in collections:
        collection = mongo_db[collection_name]
        documents = list(collection.find({}))
        # Convert ObjectId to string for JSON serialization
        for doc in documents:
            doc['_id'] = str(doc['_id'])
        mongo_data[collection_name] = documents
        print(f"✅ Retrieved {len(documents)} documents from {collection_name}")
    
    return mongo_data

def save_to_hdfs(data, filename):
    print(f"💾 Saving {filename} to HDFS...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    hdfs_path = f'/data/{filename}_{timestamp}.json'
    
    # Convert data to JSON string
    json_data = json.dumps(data, indent=2)
    
    # Write to HDFS
    with hdfs_client.write(hdfs_path, encoding='utf-8') as writer:
        writer.write(json_data)
    
    print(f"✅ Saved to HDFS at {hdfs_path}")
    return hdfs_path

def main():
    try:
        # Create HDFS directory if it doesn't exist
        if not hdfs_client.status('/data', strict=False):
            hdfs_client.makedirs('/data')
            print("📁 Created /data directory in HDFS")

        # Get and save MySQL data
        mysql_recipes = get_mysql_recipes()
        mysql_hdfs_path = save_to_hdfs(mysql_recipes, 'mysql_recipes')

        # Get and save MongoDB data
        mongo_data = get_mongo_data()
        mongo_hdfs_path = save_to_hdfs(mongo_data, 'mongo_data')

        print("\n✨ Data transfer completed successfully!")
        print(f"📍 MySQL data location: {mysql_hdfs_path}")
        print(f"📍 MongoDB data location: {mongo_hdfs_path}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        mysql_conn.close()
        mongo_client.close()

if __name__ == "__main__":
    main() 