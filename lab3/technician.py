import sys
import pika
import time


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
        print('I\'m ready for examinations! Accepted: ' + ' and '.join(self.examinations))
        print('...')
        self.channel.start_consuming()

    @staticmethod
    def examine_callback(ch, method, props, body):
        msg = body.decode()
        examination = msg.split()[0]
        name = msg.split()[1]

        print(f'Received <<{msg}>> - start')
        time.sleep(2)
        print('Processed')
        resp = f'{name} {examination} done'

        ch.basic_publish(exchange='responses',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=resp)
        ch.basic_ack(delivery_tag=method.delivery_tag)


def wake_technician(args):

    examinations = []
    for i in range(1, len(args)):
        examinations.append(args[i])

    return Technician(examinations)


def main():
    tech = wake_technician(sys.argv)


if __name__ == '__main__':
    main()
