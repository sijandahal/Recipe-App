# Dockerfile (consumer)
FROM python:3.10-slim
WORKDIR /app

COPY kafka_to_mysql.py .
COPY kafka_producer.py .
RUN pip install kafka-python mysql-connector-python pandas

# COPY large file LAST to avoid rebuilds when not changed
CMD ["python", "kafka_to_mysql.py"]
