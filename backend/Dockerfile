FROM bitnami/spark:latest as spark
FROM python:3.9

# Copy Spark from the Bitnami image
COPY --from=spark /opt/bitnami/spark /opt/spark
COPY --from=spark /opt/bitnami/java /opt/java

ENV SPARK_HOME=/opt/spark
ENV JAVA_HOME=/opt/java
ENV PATH=$PATH:$SPARK_HOME/bin:$JAVA_HOME/bin
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.7-src.zip:$PYTHONPATH

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "run.py"]
