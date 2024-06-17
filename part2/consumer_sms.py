import pika
import json
import signal
import sys
from models import Contact
import connect  # Import the connect module to use the RabbitMQ connection

connection = None
channel = None

def send_sms(contact):
    # Dummy sms function )))
    print(f"Sending SMS to {contact.phone_number}")
    contact.sms_sent = True
    contact.save()

def callback(ch, method, properties, body):
    data = json.loads(body)
    contact_id = data['contact_id']
    contact = Contact.objects(id=contact_id).first()
    if contact:
        send_sms(contact)

def signal_handler(sig, frame):
    print('Shutting down gracefully...')
    if connection:
        connection.close()
    sys.exit(0)

def main():
    global connection, channel

    signal.signal(signal.SIGINT, signal_handler)
    
    connection = connect.get_rabbitmq_connection()
    if not connection:
        print('Failed to establish RabbitMQ connection.')
        sys.exit(1)

    channel = connection.channel()
    channel.queue_declare(queue='sms_queue')
    channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages. Press Ctrl+C to exit.')
    channel.start_consuming()

if __name__ == '__main__':
    main()
