FROM python:3.10-slim


# Install Java and utilities
RUN apt-get update && apt-get install -y default-jdk procps && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$JAVA_HOME/bin:$PATH

WORKDIR /app

COPY data_to_hdfs.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "data_to_hdfs.py"] 

