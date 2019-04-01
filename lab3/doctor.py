import pika


class Doctor:
    def __init__(self, queue_name):
        self.queue_name = queue_name

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.queue_name,
                                   durable=True)
        self.channel.exchange_declare(exchange='logs',
                                      exchange_type='topic')

    def go_home(self):
        self.connection.close()

    def order(self, examination, name):
        key = f'tec.{examination}'
        self.channel.basic_publish(exchange='logs',
                                   routing_key=key,
                                   body=name)
        print(f'Ordered examination: {key}, {name}')


def main():

    doctor = Doctor('hospital')
    doctor.order('knee', 'wanczyk')


if __name__ == '__main__':
    main()
