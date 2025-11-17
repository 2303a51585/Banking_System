import pytest
from models import SavingsAccount, CurrentAccount


def test_interest_applied_savings():
    acc = SavingsAccount(
        acc_number="S300",
        holder="Alice",
        balance=1200,
        interest_rate=0.06
    )

    transaction = acc.apply_interest(months=1)
    interest_added = transaction.amount

    expected = 1200 * (0.06 / 12)

    assert round(interest_added, 2) == round(expected, 2)
    assert round(acc.balance, 2) == round(1200 + expected, 2)


def test_interest_not_for_current_account():
    acc = CurrentAccount(acc_number="C300", holder="Vishal", balance=1500)

    # CurrentAccount should raise *Exception*, NOT AttributeError
    with pytest.raises(Exception):
        acc.apply_interest()
