import asyncio
import random
import uuid
import time
import threading
import pika
import names


class Doctor:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.responses = dict()
        self.response_queue = 'res.doc'
        self.waiting = 0
        self.lock = threading.Lock()

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.basic_consume(
            queue=self.response_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        # info queue
        result = self.channel.queue_declare('', exclusive=True)
        info_queue = result.method.queue
        self.channel.queue_bind(exchange='info',
                                queue=info_queue)
        self.channel.basic_consume(
            queue=info_queue, on_message_callback=self.info_callback, auto_ack=True)

    def go_home(self):
        self.connection.close()

    def order(self, examination, name):
        corr_id = str(uuid.uuid4())

        self.lock.acquire()
        self.responses[corr_id] = None
        self.lock.release()

        key = f'tec.{examination}'
        msg = f'{examination} {name}'
        print('Ordering..')
        self.channel.basic_publish(exchange='examinations',
                                   routing_key=key,
                                   properties=pika.BasicProperties(
                                       reply_to=self.response_queue,
                                       correlation_id=corr_id,
                                   ),
                                   body=msg)
        print(f'Ordered examination: {examination} {name}')

        self.waiting += 1
        if self.waiting == 1:
            thread = threading.Thread(target=self.wait_for_response)
            thread.start()

    def wait_for_response(self):
        while self.waiting > 0:
            print(self.waiting)
            #self.lock.acquire()
            # print('wait lock')
            self.connection.process_data_events()
            for key in self.responses:
                if self.responses[key]:
                    print(self.responses[key])
                    self.waiting -= 1

            # print('wait released')
            #self.lock.release()
            time.sleep(1)

    def on_response(self, ch, method, props, body):
        corr_id = props.correlation_id
        self.lock.acquire()
        print('resp lock')
        if corr_id in self.responses.keys():
            self.responses[corr_id] = body.decode()
        print('resp release')
        self.lock.release()

    @staticmethod
    def info_callback(ch, method, props, body):
        print(f'ADMIN INFO: {body.decode()}')

    def few_orders(self, count):
        for i in range(count):
            self.order('knee', names.get_first_name())


def main():
    examinations = ['knee', 'hip', 'elbow']
    doctor = Doctor('hospital')
    # doctor.order(examinations[random.randint(0, 2)], names.get_first_name())
    doctor.few_orders(2)
    print('ok')
    time.sleep(10)

    # almost solved threading problem!!!


if __name__ == '__main__':
    main()
