import random
import string
import time

import grpc
from gen import exchange_pb2_grpc
from gen import exchange_pb2
import sys
import Ice
import threading
Ice.loadSlice("../bank.ice")
from Bank import *
from helpers import *


class AccountI(Account):
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


class StandardAccountI(AccountI, StandardAccount):
    def applyForCredit(self, currency, amount, term, current):
        raise InvalidAccountExceptionI


class PremiumAccountI(AccountI, StandardAccount):
    def applyForCredit(self, currency, amount, term, current):
        if currency not in bank_currencies:
            raise InvalidCurrencyExceptionI
        main_cost = amount * rate[currency]
        print(f'Credit on amount {main_cost} accepted')
        return Credit(main_cost, amount)


class AccountFactoryI(AccountFactory):
    def __init__(self):
        self.accounts = {}

    def gen_password(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def createAccount(self, uid, balance, income, current):
        password = self.gen_password()

        if income > 110901:
            type = AccountType.premium
            account = PremiumAccountI(type, uid, balance, income, password)
        else:
            type = AccountType.standard
            account = StandardAccountI(type, uid, balance, income, password)

        print(f'Created Account {type}')
        return AccountInfo(type, password)


def subscribeForExchange():
    channel = grpc.insecure_channel('localhost:50051')
    stub = exchange_pb2_grpc.ExchangeStub(channel)

    req = exchange_pb2.ExchangeRequest(main_currency=main_currency, extra_currency=bank_currencies)

    try:
        for res in stub.subscribeForExchange(req):
            rate[currency_name[res.currency]] = res.ExchangeRate
            print(rate)
    except Exception as e:
        print(e)


def manage_accounts():
    with Ice.initialize(sys.argv) as communicator:
        adapter = communicator.createObjectAdapterWithEndpoints("AccountFactoryAdapter", "default -p 10000")
        factory = AccountFactoryI()
        adapter.add(factory, communicator.stringToIdentity("AccountFactory"))
        adapter.activate()
        print("Bank is working")
        communicator.waitForShutdown()

def main():
    exchange_thread = threading.Thread(target=subscribeForExchange)
    exchange_thread.start()

    manage_accounts()


if __name__ == '__main__':
    main_currency = sys.argv[1]
    bank_currencies = sys.argv[2:]
    rate = {}
    main()
