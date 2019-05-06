import Ice
Ice.loadSlice("../bank.ice")
from Bank import *

currency_name = [
    "PLN",
    "EUR",
    "USD",
    "GBP"
]

currency_ice = {
        'PLN': Currency.PLN,
        'GBP': Currency.GBP,
        'USD': Currency.USD,
        'EUR': Currency.EUR
}


class InvalidCredentialsExceptionI(InvalidCredentialsException):
    pass


class InvalidCurrencyExceptionI(InvalidCurrencyException):
    pass