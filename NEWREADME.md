Demo Checklist for Professor
🔹 STEP 1: Confirm Kafka Message Flow 
You already ran docker-compose up --build


Backend Flask API sent structured data to Kafka

consumer-1 processed and printed each recipe with status messages


✅ ✅ PASS

🔹 STEP 2: Confirm Recipes Were Inserted into MySQL
Run:
bash
CopyEdit
docker exec -it mysql mysql -u root -p
# Enter password: root

Then:
sql
CopyEdit
USE forkast;
SELECT COUNT(*) FROM recipes;
SELECT * FROM recipes ORDER BY id DESC LIMIT 5;

✅ This proves the Kafka → MySQL connection is working.

MySQL → HDFS Export Command
Assuming your data-transfer container handles this logic already:
✅ Run the data transfer service:
bash
CopyEdit
docker-compose up data-transfer


1. Check the files inside HDFS /data
Run this in your terminal:
bash
CopyEdit
docker exec -it namenode hdfs dfs -ls /data


Optional: Data Check (Sample)

Option 1: View Full JSON in PowerShell
Just remove the | head -20 part and run:
bash
docker exec -it namenode hdfs dfs -cat /data/mysql_recipes_20250505_045245.json

To load the JSON file from HDFS into Apache Spark, follow these steps. I’ll assume you're using PySpark inside your Spark container.

✅ Step 1: Open your Spark container
Run this in your terminal:
bash
CopyEdit
docker exec -it spark-master bash


