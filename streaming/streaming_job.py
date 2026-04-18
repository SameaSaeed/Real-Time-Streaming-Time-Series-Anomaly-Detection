import os
import json
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from sklearn.ensemble import IsolationForest
import numpy as np
from elasticsearch import Elasticsearch
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from pyspark.sql.functions import from_json, col



class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.is_trained = False
        self.training_data = []
        self.min_training_samples = 50
        
    def update_model(self, data):
        if not data: return
        self.training_data.extend(data)
        if len(self.training_data) > 1000:
            self.training_data = self.training_data[-1000:]
        
        if len(self.training_data) >= self.min_training_samples:
            self.model.fit(self.training_data)
            self.is_trained = True
    
    def detect_anomalies(self, data):
        if not self.is_trained:
            return [1] * len(data) # 1 is "normal" in IsolationForest
        return self.model.predict(data)

class StreamingAnomalyDetection:
    def __init__(self):
        # Master is now handled by spark-submit flag
        self.spark = SparkSession.builder \
            .appName("AnomalyDetection") \
            .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        
        # Robust ES connection
        es_host = os.getenv('ELASTICSEARCH_HOST', 'elasticsearch:9200')
        self.es_client = Elasticsearch([f"http://{es_host}"])
        
        self.detector = AnomalyDetector()
        self.setup_elasticsearch()
    
    def setup_elasticsearch(self):
        index_mapping = {
            "mappings": {
                "properties": {
                    "sensor_id": {"type": "keyword"},
                    "timestamp": {"type": "date"},
                    "temperature": {"type": "float"},
                    "humidity": {"type": "float"},
                    "pressure": {"type": "float"},
                    "vibration": {"type": "float"},
                    "anomaly_score": {"type": "float"},
                    "is_anomaly": {"type": "boolean"},
                    "detection_timestamp": {"type": "date"}
                }
            }
        }
        if not self.es_client.indices.exists(index="anomalies"):
            self.es_client.indices.create(index="anomalies", body=index_mapping)
    
    def process_batch(self, df, epoch_id):
        if df.isEmpty():
            return
        
        pandas_df = df.toPandas()
        features = pandas_df[['temperature', 'humidity', 'pressure', 'vibration']].values
        
        self.detector.update_model(features.tolist())
        predictions = self.detector.detect_anomalies(features)
        
        for idx, row in pandas_df.iterrows():
            is_anomaly = (predictions[idx] == -1)
            
            if is_anomaly:
                anomaly_doc = {
                    'sensor_id': row['sensor_id'],
                    'timestamp': row['timestamp'],
                    'temperature': float(row['temperature']),
                    'humidity': float(row['humidity']),
                    'pressure': float(row['pressure']),
                    'vibration': float(row['vibration']),
                    'anomaly_score': float(self.detector.model.decision_function([features[idx]])[0]) if self.detector.is_trained else 0.0,
                    'is_anomaly': True,
                    'detection_timestamp': datetime.now().isoformat()
                }
                try:
                    self.es_client.index(index="anomalies", document=anomaly_doc)
                except Exception as e:
                    print(f"ES Error: {e}")

    def run(self):
        schema = StructType([
            StructField("sensor_id", StringType(), True),
            StructField("timestamp", StringType(), True),
            StructField("temperature", FloatType(), True),
            StructField("humidity", FloatType(), True),
            StructField("pressure", FloatType(), True),
            StructField("vibration", FloatType(), True)
        ])
        
        kafka_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
        
        df = self.spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", kafka_servers) \
            .option("subscribe", "sensor-data") \
            .option("startingOffsets", "latest") \
            .load()
        
        parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")
        
        query = parsed_df.writeStream \
            .foreachBatch(self.process_batch) \
            .trigger(processingTime='5 seconds') \
            .start()
        
        print("Streaming job started and registered with Master.")
        query.awaitTermination()

if __name__ == "__main__":
    detector = StreamingAnomalyDetection()
    detector.run()
