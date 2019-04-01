import pika


class Doctor:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def go_home(self):
        self.connection.close()

    def order(self, examination):
        self.channel.basic_publish(exchange='', routing_key=self.queue_name,
                                   body=examination)
        print('Ordered examination: ' + examination)


def main():

    doctor = Doctor('hospital')
    doctor.order('test exam')


if __name__ == '__main__':
    main()
