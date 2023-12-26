```python
# Import necessary libraries
from flask import Flask, render_template, jsonify
import psycopg2
from pymongo import MongoClient

# Flask setup
app = Flask(__name__)

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

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/text_data')
def get_text_data():
    with postgres_conn.cursor() as cursor:
        query = "SELECT * FROM text_data ORDER BY timestamp DESC LIMIT 10"
        cursor.execute(query)
        text_data = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    return jsonify(text_data)

@app.route('/api/media_data/<data_type>')
def get_media_data(data_type):
    collection = mongo_db[data_type + '_data']
    media_data = list(collection.find().sort('timestamp', -1).limit(10))
    for data in media_data:
        data['_id'] = str(data['_id'])
    return jsonify(media_data)

if __name__ == "__main__":
    app.run(debug=True)
```
