```python
# Import necessary libraries
from kafka import KafkaConsumer
import json
import psycopg2
from pymongo import MongoClient

# Kafka setup
KAFKA_TOPIC = 'multimodal_data'
KAFKA_SERVER = 'localhost:9092'
consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=[KAFKA_SERVER])

# PostgreSQL setup
POSTGRES_SERVER = 'localhost'
POSTGRES_DATABASE = 'multimodal_db'
POSTGRES_USERNAME = 'postgres'
POSTGRES_PASSWORD = 'password'
postgres_conn = psycopg2.connect(
    host=POSTGRES_SERVER,
    database=POSTGRES_DATABASE,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD
)

# MongoDB setup
MONGO_SERVER = 'localhost'
MONGO_DATABASE = 'multimodal_db'
mongo_client = MongoClient(MONGO_SERVER)
mongo_db = mongo_client[MONGO_DATABASE]

def ingest_data():
    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))

        # Store text data in PostgreSQL
        if data['type'] == 'text':
            store_text_data(data)

        # Store image, audio, and video data in MongoDB
        elif data['type'] in ['image', 'audio', 'video']:
            store_media_data(data)

def store_text_data(data):
    with postgres_conn.cursor() as cursor:
        query = """
            INSERT INTO text_data (id, content, timestamp)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (data['id'], data['content'], data['timestamp']))
    postgres_conn.commit()

def store_media_data(data):
    collection = mongo_db[data['type'] + '_data']
    collection.insert_one(data)

if __name__ == "__main__":
    ingest_data()
```
