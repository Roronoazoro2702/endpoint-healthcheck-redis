import redis
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configure Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Configure MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['test_db']
collection = db['test_collection']

# Helper function: Fetch data with caching
def fetch_data_with_cache(key):
    # Check Redis cache
    cached_data = redis_client.get(key)
    if cached_data:
        print("Cache hit")
        return jsonify({"source": "cache", "data": eval(cached_data)})

    print("Cache miss")
    # Fetch from MongoDB
    record = collection.find_one({"_id": key})
    if record:
        # Store in Redis for future requests
        redis_client.set(key, str(record), ex=3600)  # Cache for 1 hour
        return jsonify({"source": "database", "data": record})

    return jsonify({"error": "Record not found"}), 404

# Helper function: Insert data
def insert_data(key, value):
    # Write to MongoDB
    collection.update_one({"_id": key}, {"$set": value}, upsert=True)
    # Invalidate the cache for the key
    redis_client.delete(key)
    return jsonify({"message": "Data inserted successfully"})

# Routes

# Get data by key
@app.route('/data/<key>', methods=['GET'])
def get_data(key):
    return fetch_data_with_cache(key)

# Insert or update data
@app.route('/data/<key>', methods=['POST'])
def add_or_update_data(key):
    value = request.json
    if not value:
        return jsonify({"error": "Invalid data"}), 400

    return insert_data(key, value)

# Health check
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

# Main entry point
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
