FROM apache/spark:3.4.0

USER root

# Create the Ivy cache directory and give permissions
RUN mkdir -p /home/spark/.ivy2 && chmod -R 777 /home/spark/.ivy2

RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY . /app/
WORKDIR /app

# Ensure Spark user owns the app directory
RUN chown -R 185:185 /app

# Switch back to the Spark user
USER 185

CMD ["/opt/spark/bin/spark-submit", \
     "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0", \
     "--master", "spark://spark-master:7077", \
     "--conf", "spark.driver.extraJavaOptions=-Divy.cache.dir=/home/spark/.ivy2", \
     "streaming_job.py"]
