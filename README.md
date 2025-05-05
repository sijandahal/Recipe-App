<!-- Updated Readme.md -->

# Forkast - Smart Meal Planner 🍱

A full-stack big data project built with React + Flask + MongoDB + Kafka + MySQL + Docker.

---

## 🚀 How to Run the App

### 📁 Step 1: Open Terminal and Navigate to Project

```bash
cd path/to/forkast
# Example:
cd "C:\Users\\Desktop\forkast"
```

---

### 🐳 Step 2: Start All Services

```bash
docker-compose up --build
```
Use `--build` only if dependencies or code changed.
For normal runs, just use:

```bash
docker-compose up
```

---

### 🧪 Step 3: Test Flask API
```bash
curl -X POST http://localhost:5000/upload-groceries ^
  -H "Content-Type: application/json" ^
  -d "{\"ingredients\": [\"rice\", \"tofu\"], \"dietary_preferences\": [\"vegan\"], \"budget\": 25}"
```

---

### 🤭 Step 4: View Data in MongoDB Compass
- **Connection URI:** `mongodb://localhost:27017`
- **Database:** `forkast`
- **Collection:** `user_inputs`
- Click the 🔄 refresh icon to see new documents.

---

### 📂 Step 5: View Inserted Recipes in MySQL
```bash
docker exec -it mysql mysql -uroot -proot forkast
```
Then in MySQL shell:
```sql
SELECT * FROM recipes;

```

---

### 🚒 Step 6: Automate Table Creation in MySQL

You have two options:

#### ✅ Option A: Auto-create from Python (in `kafka_to_mysql.py`)
Add this inside your file:
```python
def create_table_if_not_exists():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            ingredients TEXT,
            instructions TEXT,
            calories INT,
            diet VARCHAR(100)
        )
    """)
    db.commit()
```
And call it before the consuming loop:
```python
create_table_if_not_exists()
```

#### ✅ Option B: Auto-run SQL during MySQL startup
1. Create a file named `init.sql` in the project root:
```sql
CREATE DATABASE IF NOT EXISTS forkast;
USE forkast;
CREATE TABLE IF NOT EXISTS recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    ingredients TEXT,
    instructions TEXT,
    calories INT,
    diet VARCHAR(100)
);
```

2. Update `docker-compose.yml` MySQL section:
```yaml
volumes:
  - mysql-data:/var/lib/mysql
  - ./init.sql:/docker-entrypoint-initdb.d/init.sql
```

---

### 🖎️ Step 7: Kafka Operations

#### 📤 Step 7.1: Start Kafka Producer
From the consumer folder:
```bash
docker exec -it recipe-app-consumer-1 python kafka_producer.py
```
You'll see output like:
```
[1] Sent to Kafka: {...}
```

#### 📥 Step 7.2: Start Kafka Consumer
```bash
docker-compose up consumer
```
To view consumer logs:
```bash
docker-compose logs -f consumer
```

#### 📊 Step 7.3: Verify Data in MySQL
1. Connect to MySQL:
```bash
docker exec -it mysql mysql -uroot -proot forkast
```

2. Check data in MySQL:
```sql
-- Count total recipes
SELECT COUNT(*) FROM recipes;

-- View sample recipes
SELECT * FROM recipes LIMIT 5;

-- View recipe details
docker exec -it mysql mysql -uroot -proot forkast -e "SELECT COUNT(*) FROM recipes; SELECT id, title FROM recipes ORDER BY id LIMIT 5;"

### 🗄️ Step 8: Setting up HDFS and Data Transfer

#### 🐘 Step 8.1: Start HDFS Services
```bash
docker-compose up -d namenode datanode
```


<!-- transfer data to HDFS -->

docker exec -it namenode hdfs dfs -ls /data


#### 🔍 Step 8.2: Verify HDFS Status
Access the Hadoop Web UI at:
```
http://localhost:9870
```
This will show you the HDFS cluster status and allow you to browse the file system.

#### 📤 Step 8.3: Transfer Data to HDFS
1. Build the data transfer service:
```bash
docker-compose build data-transfer
```

2. Run the data transfer service:
```bash
docker-compose up data-transfer
```

This will:
- Extract data from MySQL and MongoDB
- Save it to HDFS in JSON format
- Create files in the `/data` directory

#### 📂 Step 8.4: Verify Data in HDFS
1. Through the Hadoop Web UI:
   - Navigate to Utilities > Browse Directory
   - Go to `/data` directory
   - You'll see two files:
     - `mysql_recipes_[timestamp].json`
     - `mongo_data_[timestamp].json`

2. Or through command line:
```bash
# List files in HDFS
docker exec -it namenode hdfs dfs -ls /data

# View file sizes
docker exec -it namenode hdfs dfs -du -h /data
```

#### 📊 Step 8.5: View Data Statistics
In the Hadoop Web UI, you can see:
- File sizes
- Replication factor
- Block size
- Last modified time
- File permissions

---

### 🛑 Step 9: Stop Everything
To stop the app:
```bash
Ctrl + C
```
To remove all containers and volumes:
```bash
docker-compose down --volumes --remove-orphans
```

---

## 🛠️ Project Structure
