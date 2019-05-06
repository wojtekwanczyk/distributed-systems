import sys
import Ice
Ice.loadSlice("../bank.ice")
from Bank import *
from helpers import *


def authentication(bank, args):
    while len(args) != 2:
        args = input('Need authentication. Format: uid password\n').split()
    ctx = {'password': args[1]}
    return bank.accessAccount(int(args[0]), ctx)


def main():
    port = sys.argv[1]
    with Ice.initialize(sys.argv) as communicator:
        base = communicator.stringToProxy("AccountFactory:default -p " + port)
        bank = AccountFactoryPrx.checkedCast(base)
        if not bank:
            print('Invalid proxy')
            sys.exit(1)

        while True:
            commands = input('Write command:\n')
            if not commands:
                continue
            commands = commands.split()
            command = commands[0]
            args = []

            if command == 'n':
                while len(args) != 4:
                    args = input('New user. Format: name surname uid income\n').split()
                try:
                    res = bank.createAccount(args[0], args[1], int(args[2]), float(args[3]))
                    print(f'Created {res.type} account. Password: {res.password}')
                except Exception as e:
                    print("Unable to create account. Wrong format given or account already exists.")
                continue
            if command == 'c':
                print('Credit')

                # authenticate
                try:
                    account_proxy = authentication(bank, args)
                    args = []
                except Exception as e:
                    continue

                # verify premium account
                if account_proxy.ice_isA("::Bank::StandardAccount"):
                    print('You have standard account. Cannot get a credit')
                    continue

                # get a credit
                while len(args) != 5:
                    args = input('You can get a credit. Format: currency amount years months days\n').split()
                term = Term(int(args[2]), int(args[3]), int(args[4]))
                try:
                    credit = account_proxy.applyForCredit(currency_ice[args[0]], float(args[1]), term)
                    print(f'Credit accepted.\nMain currency value: {credit.mainCurrency}\n'
                          f'{args[0]} value: {credit.foreignCurrency}')
                except Exception as e:
                    print(e)
                    print("Wrong format given or invalid currency.")
                continue
            if command == 't':
                print('Account type')

                # authenticate
                try:
                    account_proxy = authentication(bank, args)
                    args = []
                except Exception as e:
                    continue

                # get type
                try:
                    a_type = account_proxy.getAccountType()
                    print(f'Account type: {a_type}')
                except Exception as e:
                    print(e)
                continue
            if command == 'b':
                print('Account balance')

                # authenticate
                try:
                    account_proxy = authentication(bank, args)
                    args = []
                except Exception as e:
                    continue

                # get balance
                try:
                    balance = account_proxy.getAccountBalance()
                    print(f'Account balance: {balance}')
                except Exception as e:
                    print(e)
                continue


if __name__ == '__main__':
    main()
