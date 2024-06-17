from mongoengine import connect
import configparser
from mongoengine.connection import get_connection
import pika

config = configparser.ConfigParser()
config.read('config.ini')

# MongoDB configuration
mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

# RabbitMQ configuration
rabbitmq_host = config.get('RABBITMQ', 'host')
rabbitmq_port = config.get('RABBITMQ', 'port')

try:
    # Connect to MongoDB
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

def get_rabbitmq_connection():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=int(rabbitmq_port)))
        return connection
    except Exception as e:
        print(f"Failed to connect to RabbitMQ: {e}")
        return None
