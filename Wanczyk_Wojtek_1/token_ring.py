from lab1.client_udp import ClientUDP
from lab1.client_tcp import ClientTCP


def get_config(config_file):
    with open(config_file, 'r') as f:
        clients = f.read().splitlines()
    config = clients[0]
    clients = clients[1:]
    with open(config_file, 'w') as f:
        for c in clients:
            f.write(c + '\n')
    print("You are: " + str(config))
    config = config.split()

    if config[5] == 'tcp':
        return ClientTCP(config)
    else:
        return ClientUDP(config)


def release_config(config_file, client):
    ip, port = client.next_socket
    config = [client.name, str(client.port), ip, str(port), client.token, client.protocol]
    with open(config_file, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(' '.join(config) + '\n' + content)


def main():
    config_name = 'clientsTCP'
    client = get_config(config_name)
    release_config(config_name, client)


if __name__ == '__main__':
    main()
