import random
import uuid
import time
from threading import Thread
import pika
import names


class Doctor:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.responses = dict()
        self.response_queue = 'res.doc'

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.basic_consume(
            queue=self.response_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def go_home(self):
        self.connection.close()

    def order(self, examination, name):
        corr_id = str(uuid.uuid4())
        self.responses[corr_id] = None

        key = f'tec.{examination}'
        msg = f'{examination} {name}'
        self.channel.basic_publish(exchange='examinations',
                                   routing_key=key,
                                   properties=pika.BasicProperties(
                                       reply_to=self.response_queue,
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
    examinations = ['knee', 'hip', 'elbow']
    doctor = Doctor('hospital')
    doctor.order(examinations[random.randint(0, 2)], names.get_first_name())


if __name__ == '__main__':
    main()
