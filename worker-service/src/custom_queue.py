import pika
from threading import Thread


class RabbitMQ():

    def __init__(self, host: str, queue_name: str):
        self.host = host
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.thread = None

        self.routing_map = {
            "host.add": self.add_host,
            "host.update": self.update_host,
            "host.delete": self.delete_host
        }

    def _connect(self):
        if self.connection:
            raise Exception("Queue is opened.")

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()

    def _close(self):
        if not self.connection or self.connection.is_closed:
            raise Exception("Conn is closed.")

        self.connection.close()

    def _publish(self, queue_name: str, message: str):
        if not self.connection or self.connection.is_closed:
            raise Exception("Conn is closed.")

        self.channel.queue_declare(queue=queue_name)
        self.connection.publish(exchange='', body=message, routing_key=queue_name)

    def _on_message_callback(self, ch, method, properties, body):
        handler = self.routing_map.get(method.routing_key)

        if not handler:
            # TODO: logging error
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        handler(body)

    def _consume(self):
        self.channel.basic_consume(queue=self.queue_name, auto_ack=True, on_message_callback=self._on_message_callback)
        self.channel.start_consuming()

    def start_consuming(self):
        self._connect()
        self._consume()

    def add_host(self, body):
        ...

    def update_host():
        ...

    def delete_host():
        ...
