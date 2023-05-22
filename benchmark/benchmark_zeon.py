import random
import logging
from locust import HttpUser, task, between
import requests
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LAT_MIN = -90.0
LAT_MAX = 90.0
LON_MIN = -180.0
LON_MAX = 180.0

# Number of data points to generate
NUM_POINTS = 100000

# Generate random data points
data = [(random.uniform(LAT_MIN, LAT_MAX), random.uniform(LON_MIN, LON_MAX)) for _ in range(NUM_POINTS)]

# Connect to PostgreSQL database

class LocationUser(HttpUser):
    wait_time = between(0.5, 3)

    @task
    def postgres_store(self):
        lat, lon = random.choice(data)
        adata = {
            "lat": lat,
            "long": lon
        }
        loc_id = random.randint(1, 100000)
        requests.put(f'http://127.0.0.1:8000/v1/data/{loc_id}', data=json.dumps(adata))
        logger.info(f"Retrieved location ({lat}, {lon}) from Zeon Database")
