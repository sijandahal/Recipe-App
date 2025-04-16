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

### 🖎️ Step 7: Send Recipes to Kafka (Manually)
From the consumer folder:
```bash
docker exec -it forkast-consumer-1 python kafka_producer.py
```
You’ll see output like:
```
[1] Sent to Kafka: {...}
```

---

Go to sql

docker exec -it mysql mysql -uroot -proot forkast

Then in the MySQL prompt:
SELECT COUNT(*) FROM recipes;
SELECT * FROM recipes LIMIT 5;


### 🛑 Step 8: Stop Everything
To stop the app:
```bash
Ctrl + C
```
To remove all containers and volumes:
```bash
docker-compose down --volumes --remove-orphans
```

---
