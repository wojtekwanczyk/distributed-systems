module Bank {

    enum AccountType {standard, premium};
    enum Currency {PLN, EUR, USD, GBP};

    struct Credit {
        double mainCurrency;
        double foreignCurrency;
    }

    struct Term {
        short years;
        short months;
        short days;
    }

    exception InvalidCredentialsException {
        string reason;
    }

    exception InvalidCurrencyException {
        string reason;
    }

    struct AccountInfo {
        AccountType type;
        string password;
    }

    interface Account {
        AccountType getAccountType();
        double getAccountBalance();
        Credit applyForCredit(Currency currency, double amount, Term term) throws InvalidCurrencyException;
    }

    interface StandardAccount extends Account {}

    interface PremiumAccount extends Account {}

    interface AccountFactory {
        AccountInfo createAccount(string name, string surname, long uid, double income);
        Account* accessAccount(long uid) throws InvalidCredentialsException;
    }
}
