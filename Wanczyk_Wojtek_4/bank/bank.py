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
    def __init__(self, name, surname, account_type, UID, income, password, account_id):
        self.name = name
        self.surname = surname
        self.accountType = account_type
        self.id = UID
        self.balance = 0
        self.income = income
        self.password = password
        self.account_id = account_id

    def getAccountType(self, current):
        print(f'{self.account_id} inquired for account type')
        return self.accountType

    def getAccountBalance(self, current):
        print(f'{self.account_id} inquired for account balance')
        return self.balance


class StandardAccountI(AccountI, StandardAccount):
    def applyForCredit(self, currency, amount, term, current):
        raise NotImplemented


class PremiumAccountI(AccountI, PremiumAccount):
    def applyForCredit(self, currency, amount, term, current):
        if currency not in bank_currencies_ice:
            raise InvalidCurrencyExceptionI
        main_cost = amount * rate[currency]
        self.balance += main_cost
        print(f'{self.account_id} Credit on amount {main_cost} accepted')
        return Credit(main_cost, amount)


class AccountFactoryI(AccountFactory):
    def __init__(self):
        self.accounts = {}

    def gen_password(self):
        # return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        return 'admin'

    def createAccount(self, name, surname, uid, income, current):
        password = self.gen_password()
        login = str(uid) + '_' + password
        if income > 911:
            type = AccountType.premium
            account_id = str(uid) + '_' + str(type)
            account = PremiumAccountI(name, surname, type, uid, income, password, account_id)
        else:
            type = AccountType.standard
            account_id = str(uid) + '_' + str(type)
            account = StandardAccountI(name, surname, type, uid, income, password, account_id)

        self.accounts[login] = account_id
        current.adapter.add(account, Ice.stringToIdentity(account_id))
        print(f'Created account {account_id}')

        return AccountInfo(type, password)

    def accessAccount(self, uid, current):
        login = str(uid) + '_' + current.ctx['password']
        try:
            account_id = self.accounts[login]
            account_proxy = AccountPrx.checkedCast(current.adapter.createProxy(Ice.stringToIdentity(account_id)))
        except Exception:
            raise InvalidCredentialsExceptionI
        print(f'{account_id} has obtained access')
        return account_proxy


def subscribeForExchange():
    channel = grpc.insecure_channel('localhost:50051')
    stub = exchange_pb2_grpc.ExchangeStub(channel)

    req = exchange_pb2.ExchangeRequest(main_currency=main_currency, extra_currency=bank_currencies)

    try:
        for res in stub.subscribeForExchange(req):
            rate[currency_ice[currency_name[res.currency]]] = res.ExchangeRate
            print(rate)
    except Exception as e:
        print(e)


def manage_accounts():
    with Ice.initialize(sys.argv) as communicator:
        adapter = communicator.createObjectAdapterWithEndpoints("AccountFactoryAdapter", "default -p " + port)
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
    port = sys.argv[1]
    main_currency = sys.argv[2]
    bank_currencies = sys.argv[3:]
    bank_currencies_ice = []
    for c in bank_currencies:
        bank_currencies_ice.append(currency_ice[c])
    rate = {}
    main()
