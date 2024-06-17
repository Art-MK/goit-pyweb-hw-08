import pika
import json
from faker import Faker
from models import Contact
import connect

fake = Faker()

def create_fake_contact():
    contact_data = {
        "full_name": fake.name(),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "preferred_method": fake.random_element(elements=('email', 'sms'))
    }

    existing_contact = Contact.objects(
        full_name=contact_data["full_name"],
        email=contact_data["email"],
        phone_number=contact_data["phone_number"]
    ).first()

    if existing_contact:
        print(f"Contact {contact_data['full_name']} already exists. Skipping.")
        return None
    else:
        contact = Contact(**contact_data)
        contact.save()
        print(f"Contact {contact_data['full_name']} has been added.")
        return contact

def send_to_queue(queue_name, message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=connect.rabbitmq_host, port=int(connect.rabbitmq_port)))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_publish(exchange='', routing_key=queue_name, body=message)
        connection.close()
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to connect to RabbitMQ server: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    for _ in range(10):  # Create 10 fake contacts
        contact = create_fake_contact()
        if contact:
            message = json.dumps({'contact_id': str(contact.id)})
            if contact.preferred_method == 'email':
                send_to_queue('email_queue', message)
            else:
                send_to_queue('sms_queue', message)

if __name__ == '__main__':
    main()
