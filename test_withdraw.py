import pytest
from models import SavingsAccount, CurrentAccount

def test_withdraw_success():
    acc = SavingsAccount(acc_number="S200", holder="Arun", balance=1000)
    acc.withdraw(400)
    assert acc.balance == 600


def test_withdraw_insufficient_balance():
    acc = CurrentAccount(acc_number="C200", holder="Sam", balance=300)

    # withdraw(500) should raise "Insufficient balance"
    with pytest.raises(Exception) as exc:
        acc.withdraw(500)

    assert "Insufficient balance" in str(exc.value)
