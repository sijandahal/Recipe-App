import time
from kafka import KafkaConsumer
import mysql.connector
import json
import math

print("🔍 Starting consumer setup...")

# --- Add this retry logic before creating the consumer ---
max_retries = 10
for attempt in range(max_retries):
    try:
        print(f"🔄 Attempting to connect to Kafka (attempt {attempt+1}/{max_retries})...")
        consumer = KafkaConsumer(
            'recipes',
            bootstrap_servers='kafka:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            max_poll_records=10000
        )
        print("✅ Successfully connected to Kafka!")
        break  # Success!
    except Exception as e:
        print(f"❌ Kafka not available yet (attempt {attempt+1}/{max_retries}): {e}")
        time.sleep(5)
else:
    print("❌ Failed to connect to Kafka after several attempts. Exiting.")
    exit(1)
# --- End retry logic ---

# MySQL connection setup
try:
    print("🔍 Testing MySQL connection...")
    db = mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="forkast"
    )
    cursor = db.cursor()
    cursor.execute("SELECT 1")
    cursor.fetchall()  # Consume the result
    print("✅ MySQL connection successful!")
except Exception as e:
    print(f"❌ MySQL connection failed: {e}")
    exit(1)

# Create table if it doesn't exist
try:
    print("🔍 Creating recipes table if it doesn't exist...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INT PRIMARY KEY,
            title VARCHAR(255),
            ingredients TEXT,
            directions TEXT,
            link TEXT,
            source VARCHAR(255),
            NER TEXT
        )
    """)
    db.commit()
    print("✅ Recipes table ready!")
except Exception as e:
    print(f"❌ Error creating recipes table: {e}")
    exit(1)

# Helper to clean row values
def sanitize(value):
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if str(value).lower() == 'nan':
        return None
    if str(value).strip() == '':
        return None
    return value

def is_valid_recipe(data):
    required_fields = ['id', 'title', 'ingredients', 'directions', 'link', 'source', 'NER']
    for field in required_fields:
        if field not in data or not data[field] or str(data[field]).strip() == '':
            print(f"❌ Missing or empty required field: {field}")
            return False
    # Check if JSON arrays are valid
    try:
        json.loads(data['ingredients'])
        json.loads(data['directions'])
        json.loads(data['NER'])
    except Exception as e:
        print(f"❌ Invalid JSON in recipe data: {e}")
        return False
    return True

def recipe_exists(recipe_id):
    try:
        cursor.execute("SELECT 1 FROM recipes WHERE id = %s", (recipe_id,))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"❌ Error checking for duplicate recipe: {e}")
        return False

# Insert batch into MySQL
def insert_recipes(batch):
    try:
        sql = """
            INSERT INTO recipes (id, title, ingredients, directions, link, source, NER)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        sanitized_batch = [
            tuple(sanitize(field) for field in row)
            for row in batch
        ]
        cursor.executemany(sql, sanitized_batch)
        db.commit()
        print(f"✅ Successfully inserted {len(batch)} recipes into MySQL")
    except Exception as e:
        print(f"❌ Error inserting recipes into MySQL: {e}")
        db.rollback()

# Consume and insert loop
batch = []
total_inserted = 0
batch_size = 100  # Reduced from 10000 for testing

print("📡 Consumer is running and waiting for messages...")

try:
    for message in consumer:
        print(f"\n📥 Processing new message...")
        print(f"📥 Message value: {message.value}")
        data = message.value

        # Validation
        print("🔍 Validating recipe...")
        if not is_valid_recipe(data):
            print(f"❌ Invalid recipe skipped: {data.get('id', 'no id')}")
            continue
        print("✅ Recipe validation passed")

        # Deduplication
        print("🔍 Checking for duplicates...")
        if recipe_exists(data['id']):
            print(f"⚠️ Duplicate recipe id skipped: {data['id']}")
            continue
        print("✅ No duplicate found")

        row = (
            data.get("id"),
            data.get("title"),
            data.get("ingredients"),
            data.get("directions"),
            data.get("link"),
            data.get("source"),
            data.get("NER")
        )
        batch.append(row)
        print(f"📦 Added recipe {data['id']} to batch. Current batch size: {len(batch)}")

        if len(batch) >= batch_size:
            print(f"🔄 Batch size reached {batch_size}, inserting into MySQL...")
            insert_recipes(batch)
            total_inserted += len(batch)
            print(f"✅ Inserted {len(batch)} rows — Total: {total_inserted}")
            batch.clear()

except Exception as e:
    print(f"❌ Error in consumer loop: {e}")
    raise

# Insert any remaining recipes in the batch
if batch:
    print(f"🔄 Inserting final batch of {len(batch)} recipes...")
    insert_recipes(batch)
    total_inserted += len(batch)
    print(f"✅ Inserted {len(batch)} rows — Total: {total_inserted}")
