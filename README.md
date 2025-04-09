# Forkast - Smart Meal Planner 🍱

A full-stack big data project built with React + Flask + MongoDB + Docker.

---

## 🚀 How to Run the App

### 📁 Step 1: Open Terminal and Navigate to Project

```bash
cd path/to/forkast
# Example:
cd "C:\Users\\Desktop\forkast"


🐳 Step 2: Start All Services

docker-compose up --build

Use --build only if dependencies or code changed.
For normal runs, just use:

docker-compose up


🧪 Step 3: Test Flask API
curl -X POST http://localhost:5000/upload-groceries ^
  -H "Content-Type: application/json" ^
  -d "{\"ingredients\": [\"rice\", \"tofu\"], \"dietary_preferences\": [\"vegan\"], \"budget\": 25}"

🧭 Step 4: View Data in MongoDB Compass
Connection: mongodb://localhost:27017

Database: forkast

Collection: user_inputs
Click the 🔄 refresh icon to see new documents.

🛑 Step 5: Stop Everything
To stop the app:

Ctrl + C
To remove all containers:



docker-compose down
