import socket
import time


def get_config(config_file):
    with open(config_file, 'r') as f:
        clients = f.read().splitlines()
    config = clients[0]
    clients = clients[1:]
    with open(config_file, 'w') as f:
        for c in clients:
            f.write(c + '\n')
    print("You are: " + str(config))

    return Client(config.split())


def release_config(config_file, client):
    ip, port = client.next_socket
    config = [client.name, str(client.port), ip, str(port), str(client.token), client.protocol]
    with open(config_file, 'a') as f:
        f.write(' '.join(config) + '\n')


class Client(object):
    def __init__(self, config):
        self.name = config[0]
        self.port = int(config[1])
        self.next_socket = (config[2], int(config[3]))
        self.token = bool(config[4])
        self.protocol = config[5]
        self.MSG_LEN = 2048

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', self.port))

    def send(self, receiver, msg):
        msg = receiver + ' ' + msg
        self.socket.sendto(bytes(msg, 'utf-8'), self.next_socket)

    def receive(self):
        buff = []
        while not buff:
            buff = self.socket.recv(self.MSG_LEN)
        buff = str(buff, 'utf-8')
        time.sleep(1)
        print(buff)



def main():
    config_name = 'clients'
    client = get_config(config_name)

    client.send('aaa', '')
    client.receive()

    release_config(config_name, client)


if __name__ == '__main__':
    main()
