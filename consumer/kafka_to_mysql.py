# kafka_to_mysql.py
from kafka import KafkaConsumer
import mysql.connector
import json

# Kafka consumer setup
consumer = KafkaConsumer(
    'recipes',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
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

# Insert function using batch insert
def insert_recipes(batch):
    sql = """
        INSERT INTO recipes (id, title, ingredients, directions, link, source, NER)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, batch)
    db.commit()

# Start consuming in batch
print("Consumer running...")
batch = []
batch_size = 10000  # adjust for performance

for msg in consumer:
    data = msg.value
    values = (
        int(data.get("id", 0)),
        data.get("title"),
        data.get("ingredients"),
        data.get("directions"),
        data.get("link"),
        data.get("source"),
        data.get("NER")
    )
    batch.append(values)

    if len(batch) >= batch_size:
        insert_recipes(batch)
        print(f"Inserted {len(batch)} recipes into MySQL")
        batch.clear()
