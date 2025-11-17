from models import SavingsAccount, CurrentAccount, transfer

def test_transfer_between_accounts():
    src = SavingsAccount(acc_number="S400", holder="Ravi", balance=3000)
    dst = CurrentAccount(acc_number="C400", holder="Teja", balance=500)

    transfer(src, dst, 1000)

    assert src.balance == 2000
    assert dst.balance == 1500
