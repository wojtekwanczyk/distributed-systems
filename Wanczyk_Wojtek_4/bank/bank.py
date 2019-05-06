import grpc
from gen import exchange_pb2_grpc
from gen import exchange_pb2
import sys
import Ice
Ice.loadSlice("../bank.ice")
import Bank


currency = [
    "PLN",
    "EUR",
    "USD",
    "GPB"
]


class NotPremiumAccountExceptionI(Bank.NotPremiumAccountException):
    pass


class InvalidCredentialsExceptionI(Bank.InvalidCredentialsException):
    pass


class AccountI(Bank.Account):
    def __init__(self, account_type, UID, balance, income, password):
        self.accountType = account_type
        self.id = UID
        self.balance = balance
        self.income = income
        self.password = password

    def getAccountType(self, current):
        return self.accountType

    def getAccountBalance(self, current):
        return self.balance


class StandardAccount(AccountI, Bank.StandardAccount):
    def applyForCredit(self, currency, amount, term, current):
        raise NotPremiumAccountExceptionI


def main():

    main_currency = sys.argv[1]
    currencies = sys.argv[2:]

    channel = grpc.insecure_channel('localhost:50051')
    stub = exchange_pb2_grpc.ExchangeStub(channel)

    req = exchange_pb2.ExchangeRequest(main_currency=main_currency, extra_currency=currencies)

    try:
        for res in stub.subscribeForExchange(req):
            print(currency[res.currency] + ' ' + str(res.ExchangeRate))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
