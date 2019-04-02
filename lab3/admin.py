from threading import Thread

import pika


class Admin:
    def __init__(self):

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='logs', exchange_type='topic')
        result = self.channel.queue_declare('', exclusive=True)
        self.queue_name = result.method.queue

        self.channel.queue_bind(exchange='logs',
                                queue=self.queue_name,
                                routing_key='#')

        self.channel.basic_consume(queue=self.queue_name,
                                   on_message_callback=self.examine_callback,
                                   auto_ack=False)
        print('Admin is working')
        print('...')
        thread = Thread(target=self.channel.start_consuming)
        thread.start()

    @staticmethod
    def examine_callback(ch, method, properties, body):
        msg = body.decode()
        print(f'Received <<{msg}>>')


def main():
    admin = Admin()
    # todo admin msg


if __name__ == '__main__':
    main()
