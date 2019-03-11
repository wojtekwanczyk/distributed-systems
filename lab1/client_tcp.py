import select
from multiprocessing import Process, Queue
import socket
import time


class ClientTCP(object):
    def __init__(self, config):
        self.name = config[0]
        self.port = int(config[1])
        self.next_socket = (config[2], int(config[3]))
        self.token = config[4]
        self.protocol = config[5]
        self.sending_port = self.port * 2
        self.logging_port = self.sending_port + 1
        self.MSG_LEN = 2048
        self.receiver = ''
        self.debug = True
        self.sleep = True
        self.nr = 1
        if self.token == "True":
            self.nr = 1

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', self.port))
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        self.sending_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sending_socket.bind(('', self.sending_port))

        # set no delay
        self.sending_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        self.logging_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.logging_socket.bind(('', self.logging_port))

        self.msg = Queue()
        self.logger_ip = '224.0.0.1'
        self.logger_ports = [8000, 8001]

        listener = Process(target=self.listen)
        listener.start()

        print("Connecting")
        self.sending_socket.connect(self.next_socket)
        print("ok")
        next_ip, next_port = self.next_socket
        host = socket.gethostbyname(socket.gethostname())
        msg = next_ip + ' ' + str(next_port) + ' ' + host + ' ' + str(self.port)
        print("Sending new message " + msg)
        self.send('new', msg)

        self.console()


        listener.terminate()

    def send_log(self):
        msg = self.name
        for port in self.logger_ports:
            self.logging_socket.sendto(bytes(msg, 'utf-8'), (self.logger_ip, port))

    def send(self, receiver='', msg=''):
        print("NEXT SOCKET: " + str(self.next_socket))
        if receiver == 'new':
            msg = receiver + ' ' + msg + ' '
        elif receiver:
            msg = receiver + ' ' + self.name + ' ' + str(self.nr) + ' ' \
                  + str(self.nr) + ' ' + msg
        else:
            msg = 'empty'

        if self.debug:
            print('\nDEBUG passing token: ' + msg)
        self.sending_socket.send(bytes(msg, 'utf-8'))

    def receive(self):
        if self.debug:
            print('\nDEBUG waiting for token...')

        buff = self.conn.recv(self.MSG_LEN)
        buff = str(buff, 'utf-8')

        self.send_log()
        if self.debug:
            print('DEBUG I\'ve got token: <<<' + buff + '>>>')
        if self.sleep:
            time.sleep(1)

        # empty token
        if buff == 'empty':
            if self.msg.empty():
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
        if receiver == 'new':
            buff_list = buff.split()
            if self.debug:
                print(buff)
            next_socket = (buff_list[1], int(buff_list[2]))
            new_socket = (buff_list[3], int(buff_list[4]))
            if self.debug:
                print(next_socket)
                print(self.next_socket)
            if next_socket == self.next_socket:
                print('socket match')

                #   TODO

                self.next_socket = new_socket
                self.nr += 1
            else:
                self.send('', buff)
            if len(buff_list) > 5:
                buff_list = buff_list[5:]
                buff = ' '.join(buff_list)
                self.send(buff)
        elif receiver == self.name:
            buff_list = buff.split()
            sender = buff_list[1]
            ttl = int(buff_list[2])
            nr = int(buff_list[3])
            msg = ' '.join(buff.split()[4:])
            if nr != self.nr and nr < 100:
                self.nr = nr
            print(sender.upper() + ':\n\t' + msg)

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

    def listen(self):
        self.socket.listen(5)
        print("Waiting for connection on port " + str(self.port))
        self.conn, addr = self.socket.accept()
        print("connected to " + str(addr))
        self.conn.setblocking(False)

        time.sleep(1)
        self.send()

        while True:
            self.receive()

    def console(self):
        # initialize token
        #if self.token == "True":
        #    self.send()
        #else:
            #next_ip, next_port = self.next_socket
            #host = socket.gethostbyname(socket.gethostname())
            #msg = next_ip + ' ' + str(next_port) + ' ' + host + ' ' + str(self.port)
            #print("Sending new message" + msg)
            #self.send('new', msg)





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
