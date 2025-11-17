import uuid
from datetime import datetime, timezone


class Transaction:
    def __init__(self, kind, amount, description="", timestamp=None):
        self.id = str(uuid.uuid4())
        self.kind = kind  # deposit, withdraw, transfer_in, transfer_out, interest
        self.amount = float(amount)
        self.description = description
        self.timestamp = timestamp or datetime.now(timezone.utc).isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "kind": self.kind,
            "amount": self.amount,
            "description": self.description,
            "timestamp": self.timestamp
        }


class Account:
    def __init__(self, account_id=None, owner=None, balance=0.0, acc_type="account", **kwargs):
        self.account_id = account_id or str(uuid.uuid4())
        self.owner = owner
        self.balance = float(balance)
        self.transactions = []
        self.acc_type = acc_type

    def deposit(self, amount, description=""):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        t = Transaction("deposit", amount, description)
        self.transactions.append(t.to_dict())
        return t

    def withdraw(self, amount, description=""):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        t = Transaction("withdraw", amount, description)
        self.transactions.append(t.to_dict())
        return t

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "owner": self.owner,
            "balance": self.balance,
            "transactions": self.transactions,
            "acc_type": self.acc_type
        }


class SavingsAccount(Account):
    def __init__(self, **kwargs):
        interest_rate = kwargs.pop("interest_rate", 4.0)
        last_interest_applied = kwargs.pop("last_interest_applied", None)
        super().__init__(acc_type="savings", **kwargs)

        self.interest_rate = interest_rate
        self.last_interest_applied = last_interest_applied

    def apply_interest(self, months=1):
        monthly_rate = (self.interest_rate / 100) / 12
        interest = self.balance * monthly_rate * months

        if interest <= 0:
            return None

        self.balance += interest

        t = Transaction("interest", round(interest, 2), f"Interest for {months} month(s)")
        self.transactions.append(t.to_dict())
        self.last_interest_applied = datetime.now(timezone.utc).isoformat()

        return t


class CurrentAccount(Account):
    def __init__(self, **kwargs):
        overdraft_limit = kwargs.pop("overdraft_limit", 0.0)
        super().__init__(acc_type="current", **kwargs)
        self.overdraft_limit = overdraft_limit

    def apply_interest(self, *args, **kwargs):
        raise Exception("Interest not applicable")

    def withdraw(self, amount, description=""):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        if self.balance + self.overdraft_limit < amount:
            raise ValueError("Insufficient balance")

        self.balance -= amount
        t = Transaction("withdraw", amount, description)
        self.transactions.append(t.to_dict())
        return t


def transfer(from_acc: Account, to_acc: Account, amount):
    if from_acc is to_acc:
        raise ValueError("Cannot transfer to the same account")

    if amount <= 0:
        raise ValueError("Transfer amount must be positive")

    # Withdraw from sender
    from_acc.withdraw(amount, description=f"Transfer to {to_acc.account_id}")

    # Deposit to receiver
    to_acc.deposit(amount, description=f"Transfer from {from_acc.account_id}")

    # Additional explicit transfer records
    t_out = Transaction("transfer_out", amount, f"To {to_acc.account_id}")
    t_in = Transaction("transfer_in", amount, f"From {from_acc.account_id}")

    from_acc.transactions.append(t_out.to_dict())
    to_acc.transactions.append(t_in.to_dict())

    return t_out, t_in
