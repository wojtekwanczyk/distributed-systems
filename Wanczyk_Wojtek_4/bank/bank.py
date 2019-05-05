import grpc
from gen import exchange_pb2_grpc
from gen import exchange_pb2
import sys


# class Currency(Enum):
#     PLN = 0
#     EUR = 1
#     USD = 2
#     GBP = 3


def main():

    main_currency = sys.argv[1]
    currencies = sys.argv[2:]

    channel = grpc.insecure_channel('localhost:50051')
    stub = exchange_pb2_grpc.ExchangeStub(channel)

    req = exchange_pb2.ExchangeRequest(main_currency=main_currency, extra_currency=currencies)

    try:
        for res in stub.subscribeForExchange(req):
            print(res)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
