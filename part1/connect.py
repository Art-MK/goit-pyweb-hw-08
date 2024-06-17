from mongoengine import connect
import configparser
from mongoengine.connection import get_connection
import redis

config = configparser.ConfigParser()
config.read('config.ini')

#mongo
mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

#redis
redis_host = config.get('DB', 'redis_host')
redis_port = config.get('DB', 'redis_port')

try:
    # Connect to cluster on AtlasDB with connection string
    connect(
        host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority", 
        ssl=True
    )
    # Check if connection is established
    conn = get_connection()
    if conn:
        print("Connected to MongoDB successfully.")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

try:
    # Connect to Redis
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
    # Check if Redis connection is established
    redis_client.ping()
    print("Connected to Redis successfully.")
except Exception as e:
    print(f"Failed to connect to Redis: {e}")
