import sys
import Ice
Ice.loadSlice("../bank.ice")
import Bank


def main():
    with Ice.initialize(sys.argv) as communicator:
        base = communicator.stringToProxy("AccountFactory:default -p 10000")
        account_factory = Bank.AccountFactoryPrx.checkedCast(base)
        if not account_factory:
            raise RuntimeError("Invalid proxy")

        account = account_factory.createAccount(11, 12, 13)
        print(account)


if __name__ == '__main__':
    main()
