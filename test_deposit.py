from models import SavingsAccount, CurrentAccount

def test_savings_deposit():
    acc = SavingsAccount(acc_number="S100", holder="John", balance=1000)
    acc.deposit(500)
    assert acc.balance == 1500

def test_current_deposit():
    acc = CurrentAccount(acc_number="C100", holder="Meera", balance=200)
    acc.deposit(300)
    assert acc.balance == 500
