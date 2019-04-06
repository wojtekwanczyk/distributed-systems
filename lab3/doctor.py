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

        # info queue
        result = self.channel.queue_declare('', exclusive=True)
        info_queue = result.method.queue
        self.channel.queue_bind(exchange='info',
                                queue=info_queue)

        # response queue
        self.channel.queue_bind(exchange='info',
                                queue=self.response_queue)
        # consume own queue
        self.channel.basic_consume(
            queue=info_queue,
            on_message_callback=self.info_callback,
            auto_ack=True)

    def go_home(self):
        self.waiting = 0
        self.connection.close()

    def order(self, examination, name):
        corr_id = str(uuid.uuid4())

        self.lock.acquire()
        self.responses[corr_id] = None
        self.lock.release()

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

        self.waiting += 1
        if self.waiting == 1:
            thread = threading.Thread(target=self.wait_for_response)
            thread.start()

    def wait_for_response(self):
        while self.waiting > 0:
            self.lock.acquire()
            self.connection.process_data_events()

            resp_copy = self.responses.copy()
            for key in resp_copy:
                if resp_copy[key]:
                    print(resp_copy[key])
                    del self.responses[key]

            self.lock.release()
            time.sleep(0.3)

    def info_callback(self, ch, method, props, body):
        msg = body.decode()
        if 'done' in msg:
            corr_id = props.correlation_id
            if corr_id in self.responses.keys():
                self.responses[corr_id] = body.decode()
                self.waiting -= 1
        else:
            print(f'ADMIN INFO: {msg}')

    def few_orders(self, count):
        for i in range(count):
            self.order('knee', names.get_first_name())


def main():
    examinations = ['knee', 'hip', 'elbow']
    doctor = Doctor('hospital')
    # doctor.order(examinations[random.randint(0, 2)], names.get_first_name())
    doctor.few_orders(5)


if __name__ == '__main__':
    main()
