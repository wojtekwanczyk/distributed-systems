from multiprocessing import Process, Queue, Value
import socket
import time
import random


class ClientTCP(object):
    def __init__(self, config):
        self.name = config[0]
        self.port = int(config[1])
        self.next_socket = (config[2], int(config[3]))
        self.token = config[4]
        self.protocol = config[5]
        self.sending_port = self.port + 1000
        self.logging_port = self.port - 100
        self.MSG_LEN = 2048
        self.receiver = ''
        self.debug = True
        self.sleep = True
        self.nr = 100
        self.pri = 0
        if self.token == "True":
            self.nr = 1

        self.size = Value('i', 1)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', self.port))

        self.sending_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.logging_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.logging_socket.bind(('', self.logging_port))

        self.msg = Queue()
        self.logger_ip = '224.100.0.1'
        self.logger_ports = [8000, 8001]

        listener = Process(target=self.listen)
        listener.start()

        self.console()
        listener.terminate()

    def send_log(self):
        msg = self.name
        for port in self.logger_ports:
            self.logging_socket.sendto(bytes(msg, 'utf-8'), (self.logger_ip, port))

    def send(self, receiver='', msg=''):
        if receiver == 'new':
            msg = receiver + ' ' + msg + ' '
        elif receiver:
            msg = receiver + ' ' + self.name + ' ' + str(self.nr) + ' ' \
                  + str(self.nr) + ' ' + msg
        elif msg == '':
            msg = 'empty '

        if self.debug:
            print('\nDEBUG passing token: ' + msg + ' on ' + str(self.sending_socket))

        self.sending_socket.send(bytes(msg, 'utf-8'))

    def listen(self):
        self.socket.listen(5)
        if self.token == "True":
            print("accept - Waiting for connection on port " + str(self.port))
            self.conn, addr = self.socket.accept()
            print("connected to " + str(addr))
            buff = self.conn.recv(self.MSG_LEN)
            print("received: " + str(buff))

            buff = str(buff, 'utf-8')
            buff_list = buff.split()

            next_socket = (buff_list[1], int(buff_list[2]))
            new_socket = (buff_list[3], int(buff_list[4]))
            if self.debug:
                print(next_socket)
                print(self.next_socket)
            if next_socket == self.next_socket:
                print('socket match')
                self.next_socket = new_socket
                self.nr += 1
                print("NR: " + str(self.nr))

                self.sending_socket.connect(self.next_socket)
                self.send('allan', 'dziendobry')
            else:
                self.send('', buff)
        else:
            print("Connecting to next socket")
            self.sending_socket.connect(self.next_socket)
            print("ok")

            next_ip, next_port = self.next_socket
            host = 'localhost'
            msg = next_ip + ' ' + str(next_port) + ' ' + host + ' ' + str(self.port)
            print("Sending new message " + msg)
            self.send('new', msg)
            print('Waiting for response...')
            self.conn, addr = self.socket.accept()
            print('Ive got the answer!')

        while True:
            self.receive()

    def receive(self):
        self.socket.settimeout(0.01)
        try:
            conn, addr = self.socket.accept()
            print('New connection! ' + str(conn))

            # switch socket
            self.conn.shutdown(socket.SHUT_RDWR)
            self.conn.close()
            self.conn = conn

        except socket.timeout:
            pass

        buff = self.conn.recv(self.MSG_LEN)
        buff = str(buff, 'utf-8')
        buff_list = buff.split()

        self.send_log()
        if self.debug:
            print('DEBUG I\'ve got token: <<<' + buff + '>>>')
        if self.sleep:
            time.sleep(1)

        # empty token
        if buff_list[0] == 'empty':
            if len(buff_list) > 3:
                buff_list = buff_list[1:]
            else:
                if self.msg.empty():
                    self.send()
                else:
                    rec = self.msg.get()
                    msg = self.msg.get()
                    if self.debug:
                        print("\nDEBUG sending " + rec + ' ' + msg)
                    self.send(rec, msg)
                return

        receiver = buff_list[0]

        # busy token
        if receiver == 'new':
            if self.debug:
                print(buff)
            next_socket = (buff_list[1], int(buff_list[2]))
            new_socket = (buff_list[3], int(buff_list[4]))
            if self.debug:
                print(next_socket)
                print(self.next_socket)
            if next_socket == self.next_socket:
                print('socket match')
                self.next_socket = new_socket
                self.nr += 1
                print("NR: " + str(self.nr))

                # change sending socket
                self.sending_socket.shutdown(socket.SHUT_RDWR)
                self.sending_socket.close()
                self.sending_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sending_socket.connect(self.next_socket)

                self.send('', 'size ' + str(self.nr))
            else:
                self.send('', buff)
            if len(buff_list) > 5:
                buff_list = buff_list[5:]
                buff = ' '.join(buff_list)
                self.send(buff)
        elif receiver == self.name:
            sender = buff_list[1]
            ttl = int(buff_list[2])
            nr = int(buff_list[3])
            msg = ' '.join(buff_list[4:])
            if nr != self.nr and nr < 100:
                self.nr = nr
            print(sender.upper() + ':\n\t' + msg)

            # send response
            if self.msg.empty():
                self.send('', 'cos cos ' + str(random.randint(0, 100) % self.nr + 1) + ' ' + str(self.nr))
            else:
                self.send(self.msg.get(), self.msg.get())
        elif receiver == 'size':
            self.nr = int(buff_list[1])
            # send response
            if self.msg.empty():
                self.send()
            else:
                self.send(self.msg.get(), self.msg.get())
        else:
            # pass message
            buff_list = buff.split()
            ttl = int(buff_list[2])
            ttl -= 1
            if ttl == 0:
                if self.debug:
                    print("\nDEBUG Dropping message: " + buff)
                self.send()
                return
            buff_list[2] = str(ttl)
            buff = ' '.join(buff_list)
            self.send('', buff)
            self.pri += 1

    def console(self):
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
