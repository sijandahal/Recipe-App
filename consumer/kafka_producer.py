from kafka import KafkaProducer
import pandas as pd
import json
import time

KAFKA_BROKER = 'kafka:9092'
TOPIC = 'recipes'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Chunked reading
chunk_size = 1000
total_rows = 0

print("📦 Starting to stream CSV in chunks...")

for chunk in pd.read_csv('mainrecepie.csv', chunksize=chunk_size, engine='python', dtype=str):
    for _, row in chunk.iterrows():
        producer.send(TOPIC, value=row.to_dict())
        total_rows += 1

    print(f"📤 Sent {total_rows} rows so far...")
    time.sleep(0.1)  # Throttle slightly

producer.flush()
print(f"✅ Finished sending {total_rows} rows to Kafka.")
