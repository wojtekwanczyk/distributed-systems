module Bank {

    struct UID {
        long value;
    }

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

    exception NotPremiumAccountException {
        string reason;
    }

    exception InvalidCredentialsException {
        string reason;
    }

    struct AccountInfo {
        AccountType type;
        string password;
    }

    interface Account {
        AccountType getAccountType();
        double getAccountBalance();
        Credit applyForCredit(Currency currency, double amount, Term term) throws NotPremiumAccountException;
    }

    interface StandardAccount extends Account {}

    interface PremiumAccount extends Account {}

    interface AccountFactory {
        AccountInfo createAccount(UID uid, double balance, double income);
        Account* getAccount(UID uid) throws InvalidCredentialsException;
    }
}