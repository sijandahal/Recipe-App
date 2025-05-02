# spark-scripts/export_to_hdfs.py
from pymongo import MongoClient
import pandas as pd
import os

# Connect to MongoDB
client = MongoClient("mongodb://mongo:27017")
db = client["forkast"]
collection = db["user_inputs"]

# Fetch data
docs = list(collection.find({}, {"_id": 0}))
df = pd.DataFrame(docs)

# Save to CSV locally
csv_path = "/app/user_inputs.csv"
df.to_csv(csv_path, index=False)

print("✅ MongoDB data exported to CSV at", csv_path)
print("📌 Now run:")
print("   docker cp spark-scripts/user_inputs.csv namenode:/user_inputs.csv")
print("   docker exec -it namenode hdfs dfs -mkdir -p /user_inputs")
print("   docker exec -it namenode hdfs dfs -put -f /user_inputs.csv /user_inputs/")
