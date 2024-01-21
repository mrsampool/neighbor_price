import pika
from components.event_manager.event_body import EventBody
from components.event_manager.event_manager import EventManager


class EventManagerPika(EventManager):
    def __init__(self, host: str = None, queue_name: str = None):
        self.host = host
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=host, blocked_connection_timeout=300))
        self.channel = self.conn.channel()
        self.channel.queue_declare(queue_name)
        self.queue_name = queue_name

    def publish(self, body: EventBody):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=body.to_json().encode('utf-8')
        )

    def consume(self, callback):
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=callback,
            auto_ack=False
        )
        self.channel.start_consuming()
