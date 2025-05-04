FROM python:3.10-slim

WORKDIR /app

COPY data_to_hdfs.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "data_to_hdfs.py"] 