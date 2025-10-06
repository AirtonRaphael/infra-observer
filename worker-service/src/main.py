from custom_queue import RabbitMQ


def main():
    ...


if __name__ == '__main__':
    queue = RabbitMQ('localhost', 'hosts')


    queue.start_consuming()

