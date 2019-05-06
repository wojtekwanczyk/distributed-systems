import Ice
Ice.loadSlice("../bank.ice")
import Bank

currency_name = [
    "PLN",
    "EUR",
    "USD",
    "GBP"
]


class InvalidAccountExceptionI(Bank.InvalidAccountException):
    pass


class InvalidCredentialsExceptionI(Bank.InvalidCredentialsException):
    pass


class InvalidCurrencyExceptionI(Bank.InvalidCurrencyException):
    pass