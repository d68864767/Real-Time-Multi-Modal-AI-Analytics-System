```python
# Import necessary libraries
import time
import psycopg2
from pymongo import MongoClient
from datetime import datetime, timedelta

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

def monitor_system():
    while True:
        print("Monitoring system performance...")

        # Monitor PostgreSQL database
        with postgres_conn.cursor() as cursor:
            query = "SELECT COUNT(*) FROM text_data WHERE timestamp > %s"
            cursor.execute(query, (datetime.now() - timedelta(minutes=5),))
            text_data_count = cursor.fetchone()[0]
            print(f"Number of text data processed in the last 5 minutes: {text_data_count}")

        # Monitor MongoDB database
        for data_type in ['image', 'audio', 'video']:
            collection = mongo_db[data_type + '_data']
            media_data_count = collection.count_documents({'timestamp': {'$gt': datetime.now() - timedelta(minutes=5)}})
            print(f"Number of {data_type} data processed in the last 5 minutes: {media_data_count}")

        # Sleep for 5 minutes
        time.sleep(300)

if __name__ == "__main__":
    monitor_system()
```
