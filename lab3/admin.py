from threading import Thread

import pika


class Admin:
    def __init__(self, queues):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.tec_queues = list(map(lambda x: 'tec.' + x, queues + ['adm']))
        self.res_queues = list(map(lambda x: 'res.' + x, ['doc', 'adm']))

    @staticmethod
    def examination_callback(ch, method, properties, body):
        msg = body.decode()
        print(f'Received <<{msg}>>')

    def declare_exchange(self):
        self.channel.exchange_declare(exchange='examinations', exchange_type='topic')
        self.channel.exchange_declare(exchange='responses', exchange_type='topic')
        self.channel.exchange_declare(exchange='info', exchange_type='fanout')

    def declare_queues(self):
        for queue in self.tec_queues + self.res_queues + ['info_q']:
            self.channel.queue_declare(queue=queue, durable=True)

    def bind_queues(self):
        for queue in self.tec_queues:
            self.channel.queue_bind(exchange='examinations',
                                    queue=queue,
                                    routing_key=queue)
        for queue in self.res_queues:
            self.channel.queue_bind(exchange='responses',
                                    queue=queue,
                                    routing_key=queue)
        # admin bindings
        self.channel.queue_bind(exchange='examinations',
                                queue='tec.adm',
                                routing_key='tec.*')
        self.channel.queue_bind(exchange='responses',
                                queue='res.adm',
                                routing_key='res.*')

    def start_consuming(self):
        self.channel.basic_consume(queue='tec.adm',
                                   on_message_callback=self.examination_callback,
                                   auto_ack=True)
        self.channel.basic_consume(queue='res.adm',
                                   on_message_callback=self.examination_callback,
                                   auto_ack=True)
        thread = Thread(target=self.channel.start_consuming)
        thread.start()
        print('Admin is working')
        print('...')

    def info(self, msg):
        self.channel.basic_publish(exchange='info',
                                   routing_key='',
                                   body=msg)
        print(f"Info sent: {msg}")


def main():
    exam_queues = ['knee', 'hip', 'elbow']
    print(exam_queues)

    admin = Admin(exam_queues)
    admin.declare_exchange()
    admin.declare_queues()
    admin.bind_queues()

    admin.start_consuming()

    while True:
        cmd = input()
        admin.info(cmd)


if __name__ == '__main__':
    main()
