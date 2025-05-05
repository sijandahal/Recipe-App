FROM apache/spark:3.5.1

USER root
RUN mkdir -p /opt/spark/logs && \
    chown -R spark:spark /opt/spark/logs

USER spark

ENV SPARK_HOME=/opt/spark
ENV SPARK_WORKER_CORES=2
ENV SPARK_WORKER_MEMORY=1G
ENV SPARK_WORKER_PORT=8081
ENV SPARK_WORKER_WEBUI_PORT=8081

ENTRYPOINT ["/opt/spark/sbin/start-worker.sh"]
CMD ["spark://spark-master:7077"] 