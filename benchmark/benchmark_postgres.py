import random
import time
import logging
import psycopg2
import redis
from locust import HttpUser, task, between

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PostgreSQL database configuration
DATABASE_URI = "postgresql://postgres:Deadcoder11u2@db.xkmngqfrkgxvrmgikfbi.supabase.co:5432/postgres"

# Redis configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379

# Location range for random data generation
LAT_MIN = -90.0
LAT_MAX = 90.0
LON_MIN = -180.0
LON_MAX = 180.0

# Number of data points to generate
NUM_POINTS = 100000

# Generate random data points
data = [(random.uniform(LAT_MIN, LAT_MAX), random.uniform(LON_MIN, LON_MAX)) for _ in range(NUM_POINTS)]

# Connect to PostgreSQL database
pg_conn = psycopg2.connect(DATABASE_URI)

# Connect to Redis server
redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# Initialize PostgreSQL table
with pg_conn.cursor() as cursor:
    cursor.execute("CREATE TABLE IF NOT EXISTS locations (id SERIAL PRIMARY KEY, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION)")
    pg_conn.commit()

# Initialize Redis keys
for i in range(NUM_POINTS):
    redis_conn.set(f"location_{i}", f"{data[i][0]},{data[i][1]}")

class LocationUser(HttpUser):
    wait_time = between(0.5, 3)

    @task
    def postgres_store(self):
        # Get a random data point
        lat, lon = random.choice(data)

        # Store the data point in PostgreSQL
        with pg_conn.cursor() as cursor:
            cursor.execute("INSERT INTO locations (latitude, longitude) VALUES (%s, %s)", (lat, lon))
            pg_conn.commit()
            logger.info(f"Stored location ({lat}, {lon}) in PostgreSQL")
        time.sleep(random.uniform(1, 1))

    @task
    def postgres_retrieve(self):
        # Get a random data point
        lat, lon = random.choice(data)

        # Retrieve the data point from PostgreSQL
        with pg_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM locations WHERE latitude = %s AND longitude = %s", (lat, lon))
            result = cursor.fetchone()
            if result is not None:
                logger.info(f"Retrieved location ({lat}, {lon}) from PostgreSQL")
            else:
                logger.warning(f"Location ({lat}, {lon}) not found in PostgreSQL")
        time.sleep(random.uniform(1, 1))
