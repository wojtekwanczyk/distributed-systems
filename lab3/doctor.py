import uuid
import time
from threading import Thread
import pika
import names


class Doctor:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.responses = dict()

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='logs',
                                      exchange_type='topic')

        result = self.channel.queue_declare('', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def go_home(self):
        self.connection.close()

    def order(self, examination, name):
        corr_id = str(uuid.uuid4())
        self.responses[corr_id] = None

        key = f'tec.{examination}'
        msg = f'{examination} {name}'
        self.channel.basic_publish(exchange='logs',
                                   routing_key=key,
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=corr_id,
                                   ),
                                   body=msg)
        print(f'Ordered examination: {examination} {name}')

        thread = Thread(target=self.wait_for_response, args=(corr_id,))
        thread.start()

    def wait_for_response(self, corr_id):
        while self.responses[corr_id] is None:
            self.connection.process_data_events()
        print(f'Received response: {self.responses[corr_id]}')

    def on_response(self, ch, method, props, body):
        corr_id = props.correlation_id
        if corr_id in self.responses.keys():
            self.responses[corr_id] = body.decode()


def main():

    doctor = Doctor('hospital')
    doctor.order('knee', names.get_first_name())


if __name__ == '__main__':
    main()
