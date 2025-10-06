import pika


class RabbitMQ():
    connection = None

    def __init__(self, host: str, queue_name: str):
        self.host = host
        self.queue_name = queue_name
        self.channel = None
        self.thread = None

        self.exchange_name = 'host'
        self.routing_map = [
            "host.add",
            "host.update",
            "host.delete"
        ]

    def connect_exchange(self, exchange: str):
        self.channel.exchange_declare(
            exchange=exchange,
            exchange_type='direct',
            durable=True,
            auto_delete=False,
            internal=False,
            arguments=None
        )

    def _close(cls):
        if not cls.connection or cls.connection.is_closed:
            raise Exception("Conn is closed.")

        cls.connection.close()

    def connect(self):
        if self.__class__.connection:
            raise Exception("Queue is opened.")

        self.__class__.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.queue_name)

        self.connect_exchange(self.exchange_name)

        for routing in self.routing_map:
            self.channel.queue_bind(queue=self.queue_name, exchange=self.exchange_name, routing_key=routing)

    def publish(self, routing_key: str, message: str):
        connection = self.__class__.connection
        if not connection or connection.is_closed:
            raise Exception("Conn is closed.")

        self.channel.basic_publish(exchange=self.exchange_name, body=message, routing_key=routing_key)


queue = None


def start_queue():
    global queue

    queue = RabbitMQ('localhost', 'hosts')
    queue.connect()


def get_queue():
    yield queue
