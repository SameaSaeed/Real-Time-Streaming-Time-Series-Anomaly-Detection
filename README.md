# Real-time Anomaly Detection Pipeline

## 📌 Overview

The **Real-time Anomaly Detection Pipeline** is a distributed streaming system that ingests live sensor data, detects anomalies in real time, and makes the results available through APIs and dashboards within seconds.

This project demonstrates how modern streaming technologies and online machine learning techniques can be combined to build a production-style real-time analytics pipeline.

---

## 🛠 Technologies

- **Apache Kafka** – Real-time data ingestion  
- **Apache Spark Streaming** – Stream processing and anomaly detection  
- **Python** – Data generation, preprocessing, ML logic, and APIs  
- **Elasticsearch** – Storage and indexing of detected anomalies  
- **Kibana** – Visualization and monitoring  
- **Docker & Docker Compose** – Containerized deployment and orchestration  

---

## 🧠 Problem Description

In real-world systems such as IoT monitoring, industrial systems, and financial platforms, detecting abnormal behavior as soon as it occurs is critical.

This project builds a **real-time streaming pipeline** that:
- Continuously ingests sensor data
- Preprocesses and normalizes streaming messages
- Detects anomalies using an online anomaly detection approach
- Stores only relevant anomaly events
- Exposes APIs and dashboards for monitoring and analysis

---

## 🏗 System Architecture


### Component Responsibilities

- **Producer**: Simulates live sensor data with normal and anomalous behavior  
- **Kafka**: Acts as a fault-tolerant message broker  
- **Spark Streaming**: Consumes Kafka streams, preprocesses data, and performs anomaly detection  
- **Elasticsearch**: Stores detected anomalies for fast querying  
- **REST API**: Provides endpoints to query recent anomalies  
- **Kibana**: Visualizes anomaly data in real time  

---

## ⚙️ Key Features

- Real-time ingestion of sensor data using Kafka topics  
- Stream-level preprocessing and normalization  
- Online anomaly detection suitable for continuous data streams  
- Persistent anomaly storage using Elasticsearch  
- REST endpoints for querying anomaly data  
- Fully Dockerized setup for reproducible deployment  

---

## 📦 Deliverables

- Kafka topic producer simulator  
- Spark Streaming job code  
- Online anomaly detection logic  
- Elasticsearch index setup and storage  
- REST service with example query endpoints  
- Docker Compose–based deployment instructions  

---

## 🚀 Getting Started

### Prerequisites
- Docker  
- Docker Compose  

### Run the Pipeline Locally

```bash
git clone https://github.com/vijay-illuru/Real-time-Anomaly-Detection-Pipeline.git
cd Real-time-Anomaly-Detection-Pipeline
docker compose up --build
```
## Monitor Anomalies
- **API**: http://localhost:5000/anomalies/recent
- **Kibana**: http://localhost:5601 (create index pattern: `anomalies`)
- **Logs**: `docker-compose logs -f streaming`

<img width="700" height="305" alt="spark_ui" src="https://github.com/user-attachments/assets/57ad55c5-3881-437c-8367-5587005dda6c" />

<img width="376" height="378" alt="api" src="https://github.com/user-attachments/assets/e7af4270-fee2-464c-9e9d-1f08094beba0" />

<img width="257" height="139" alt="elastic_search" src="https://github.com/user-attachments/assets/e1991035-b44f-4822-84a9-045232036864" />

<img width="955" height="406" alt="kibana" src="https://github.com/user-attachments/assets/e7b573de-283e-462d-9efc-a193c49aa0f6" />


## Stop Pipeline
```bash
docker-compose down -v
```

# Quick Deployment Guide

## Prerequisites
- Docker and Docker Compose installed
- At least 4GB RAM available for containers

## Start Pipeline
```bash
# Option 1: Use the automated start script
./start.sh

# Option 2: Manual startup
docker-compose up -d
sleep 30
./scripts/setup_elasticsearch.sh
```

## Verify Deployment
```bash
# Check all services are running
docker-compose ps

# Test API endpoints
python3 test_pipeline.py

# Manual API tests
curl http://localhost:5000/health
curl http://localhost:5000/anomalies/recent?minutes=5
```

