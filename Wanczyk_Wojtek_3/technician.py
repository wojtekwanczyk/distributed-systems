import sys
import pika
import time
import random


'''
Run with available examinations as program arguments
Available examinations: hip, elbow, knee
'''


class Technician:
    def __init__(self, examinations):
        self.examinations = examinations

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        for exam in examinations:
            self.channel.basic_consume(queue=f'tec.{exam}',
                                       on_message_callback=self.examine_callback,
                                       auto_ack=False)

        # own queue
        result = self.channel.queue_declare('', exclusive=True)
        own_queue = result.method.queue
        self.channel.queue_bind(exchange='whole_staff',
                                queue=own_queue)
        self.channel.basic_consume(
            queue=own_queue, on_message_callback=self.message_callback, auto_ack=True)

        print('I\'m ready for examinations! Accepted: ' + ' and '.join(self.examinations))
        print('...')
        self.channel.start_consuming()

    @staticmethod
    def examine_callback(ch, method, props, body):
        msg = body.decode()
        examination = msg.split()[0]
        name = msg.split()[1]

        print(f'Received <<{msg}>> - start')
        time.sleep(random.randint(0, 10))
        print('Processed')
        resp = f'{name} {examination} done'

        ch.basic_publish(exchange='whole_staff',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=resp)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def message_callback(ch, method, props, body):
        msg = body.decode()
        if 'done' not in msg:
            print(f'ADMIN INFO: {msg}')


def parse_examinations(args):
    examinations = []
    for i in range(1, len(args)):
        examinations.append(args[i])

    return examinations


def main():
    examinations = parse_examinations(sys.argv)
    tech = Technician(examinations)


if __name__ == '__main__':
    main()
