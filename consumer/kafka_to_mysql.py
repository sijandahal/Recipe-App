from kafka import KafkaConsumer
import mysql.connector
import json
import math

# Kafka consumer setup
consumer = KafkaConsumer(
    'recipes',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    max_poll_records=10000
)

# MySQL connection setup
db = mysql.connector.connect(
    host="mysql",
    user="root",
    password="root",
    database="forkast"
)
cursor = db.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INT,
        title VARCHAR(255),
        ingredients TEXT,
        directions TEXT,
        link TEXT,
        source VARCHAR(255),
        NER TEXT
    )
""")
db.commit()

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

# Insert batch into MySQL
def insert_recipes(batch):
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

# Consume and insert loop
batch = []
total_inserted = 0

print("📡 Consumer is running...")

for message in consumer:
    data = message.value
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

    if len(batch) >= 10000:
        insert_recipes(batch)
        total_inserted += len(batch)
        print(f"✅ Inserted {len(batch)} rows — Total: {total_inserted}")
        batch.clear()
