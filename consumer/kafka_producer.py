from kafka import KafkaProducer
import pandas as pd
import json
import time

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    compression_type='gzip',
    linger_ms=100,
    batch_size=65536
)

chunksize = 20000
total_sent = 0
start = time.time()

print("📦 Starting high-speed Kafka ingestion...")

for chunk_index, chunk in enumerate(pd.read_csv('mainrecepie.csv', dtype=str, chunksize=chunksize, low_memory=False)):
    records = chunk.to_dict(orient='records')
    futures = []

    for record in records:
        futures.append(producer.send('recipes', value=record))

    for future in futures:
        try:
            future.get(timeout=10)
        except Exception as e:
            print(f"⚠️ Kafka send error: {e}")

    producer.flush()
    total_sent += len(records)
    print(f"✅ Chunk {chunk_index + 1}: Sent {len(records)} records — Total: {total_sent}")

producer.flush()
end = time.time()
print(f"🚀 Done! Sent {total_sent} records in {round(end - start, 2)} seconds.")
