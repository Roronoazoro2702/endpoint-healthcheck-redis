# Redis Cache with Flask and MongoDB

## Features
- **Caching with Redis**: Speeds up data retrieval by caching results.
- **Database with MongoDB**: Stores data persistently.
- **Health Check Endpoint**: Ensures the application is running.
- **RESTful API**: Provides endpoints for fetching, inserting, and updating data.

## Dependencies
- Python 3.x
- Flask
- Redis
- MongoDB

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Roronoazoro2702/endpoint-healthcheck-redis.git
   cd endpoint-healthcheck-redis
   ```

2. **Install Required Python Packages**:
   ```bash
   pip install flask redis pymongo
   ```

3. **Start Redis and MongoDB**:
   Ensure both Redis and MongoDB are installed and running on your system.

4. **Run the Application**:
   ```bash
   python main.py
   ```

5. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:5000/`.

## Endpoints
- **GET /data/<key>**: Fetch data for a given key (uses cache or database).
- **POST /data/<key>**: Insert or update data for a given key.
- **GET /health**: Check the health of the application.
