import sys
import pika
import time


'''
Run with available examinations as program arguments
Available examinations: hip, elbow, knee
'''


class Technician:
    def __init__(self, queue_name, examinations):
        self.examinations = examinations
        self.queue_name = queue_name

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='logs', exchange_type='topic')
        result = self.channel.queue_declare(queue=self.queue_name, durable=True)
        #self.queue_name = result.method.queue

        for e_type in self.examinations:
            self.channel.queue_bind(exchange='logs',
                                    queue=self.queue_name,
                                    routing_key=f'tec.{e_type}')

        self.channel.basic_consume(queue=self.queue_name,
                                   on_message_callback=self.examine_callback,
                                   auto_ack=False)
        print('I\'m ready for examinations! Accepted: ' + ' and '.join(self.examinations))
        print('...')
        self.channel.start_consuming()

    @staticmethod
    def examine_callback(ch, method, properties, body):
        msg = body.decode()
        print(f'Received <<{msg}>> - start')
        time.sleep(10)
        print('Processed')
        ch.basic_ack(delivery_tag=method.delivery_tag)


def wake_technician(queue_name, args):

    examinations = []
    for i in range(1, len(args)):
        examinations.append(args[i])

    return Technician(queue_name, examinations)


def main():
    tech = wake_technician('hospital', sys.argv)


if __name__ == '__main__':
    main()
