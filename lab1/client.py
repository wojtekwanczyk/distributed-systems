from multiprocessing import Process, Queue
import socket
import time


class Client(object):
    def __init__(self, config):
        self.name = config[0]
        self.port = int(config[1])
        self.next_socket = (config[2], int(config[3]))
        self.token = bool(config[4])
        self.protocol = config[5]
        self.MSG_LEN = 2048
        self.receiver = ''
        self.debug = True

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', self.port))

        self.msg = Queue()

        listener = Process(target=self.listen)
        listener.start()
        self.console()
        listener.terminate()

    def send(self, receiver='', msg=''):
        if receiver:
            msg = receiver + ' ' + self.name + ' ' + msg
        else:
            msg = ''

        if self.debug:
            print('\nDEBUG passing token: ' + msg)
        self.socket.sendto(bytes(msg, 'utf-8'), self.next_socket)

    def receive(self):
        if self.debug:
            print('\nDEBUG waiting for token...')

        buff = self.socket.recv(self.MSG_LEN)
        buff = str(buff, 'utf-8')
        if self.debug:
            print('DEBUG I\'ve got token: <<<' + buff + '>>>')
        time.sleep(2)

        # empty token
        if not buff:
            if self.msg.empty():
                if self.debug:
                    print("\nDEBUG Passing empty token")
                self.send()
            else:
                rec = self.msg.get()
                msg = self.msg.get()
                if self.debug:
                    print("\nDEBUG sending " + rec + ' ' + msg)
                self.send(rec, msg)
            return

        receiver = buff.split()[0]

        # busy token
        if receiver == self.name:
            sender = buff.split()[1]
            msg = ' '.join(buff.split()[2:])
            print(sender.upper() + ':\n\t' + msg)

            # send response
            if self.msg.empty():
                self.send()
            else:
                self.send(self.msg.get(), self.msg.get())

        else:
            # pass message
            self.send(buff)

    def listen(self):
        while True:
            self.receive()

    def console(self):
        # initialize token
        if self.token:
            self.token = False
            self.send()

        self.receiver = input('Receiver: ')
        while True:
            content = input()
            if content == 'end':
                break
            if content == 'recv':
                self.receiver = input('Receiver: ')
            elif content:
                self.msg.put(self.receiver)
                self.msg.put(content)
