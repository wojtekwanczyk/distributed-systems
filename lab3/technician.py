import sys
import pika


'''
Run with available examinations as program arguments
Available examinations: hip, elbow, knee
'''


class Technician:
    def __init__(self, queue_name, examinations):
        self.queue_name = queue_name
        self.examinations = examinations

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

        self.channel.basic_consume(queue=self.queue_name,
                                   on_message_callback=self.examine_callback,
                                   auto_ack=True)
        print('I\'m ready for examinations! Accepted: ' + ' and '.join(self.examinations))
        print('...')
        self.channel.start_consuming()

    @staticmethod
    def examine_callback(ch, method, properties, body):
        msg = body.decode()
        print("Received " + msg)

    def go_home(self):
        self.connection.close()


def wake_technician(args, queue_name):

    examinations = []
    for i in range(1, len(args)):
        examinations.append(args[i])

    return Technician(queue_name, examinations)


def main():
    tech = wake_technician(sys.argv, 'hospital')


if __name__ == '__main__':
    main()
