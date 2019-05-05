import grpc
from gen import exchange_pb2_grpc


def main():

    channel = grpc.insecure_channel('localhost:50051')
    stub = exchange_pb2_grpc.ExchangeStub(channel)


if __name__ == '__main__':
    main()
