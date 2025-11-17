import unittest
from models import Account, SavingsAccount, CurrentAccount, transfer

class TestBankAccounts(unittest.TestCase):
    # Withdraw Tests
    def test_withdraw_normal_base_account(self):
        acc = Account(balance=100.0, owner="test")
        transaction = acc.withdraw(50.0, "Test withdrawal")
        self.assertAlmostEqual(acc.balance, 50.0)
        self.assertEqual(transaction.kind, "withdraw")
        self.assertEqual(transaction.amount, 50.0)
        self.assertEqual(transaction.description, "Test withdrawal")
        self.assertEqual(len(acc.transactions), 1)

    def test_withdraw_normal_savings_account(self):
        acc = SavingsAccount(balance=100.0, owner="test")
        transaction = acc.withdraw(50.0, "Test withdrawal")
        self.assertAlmostEqual(acc.balance, 50.0)
        self.assertEqual(transaction.kind, "withdraw")
        self.assertEqual(transaction.amount, 50.0)
        self.assertEqual(len(acc.transactions), 1)

    def test_withdraw_insufficient_base_account(self):
        acc = Account(balance=50.0, owner="test")
        with self.assertRaises(ValueError) as ctx:
            acc.withdraw(100.0)
        self.assertIn("Insufficient funds", str(ctx.exception))

    def test_withdraw_insufficient_current_account(self):
        acc = CurrentAccount(balance=50.0, owner="test")
        with self.assertRaises(ValueError) as ctx:
            acc.withdraw(100.0)
        self.assertIn("Insufficient funds", str(ctx.exception))

    def test_withdraw_overdraft_allowed_current_account(self):
        acc = CurrentAccount(balance=50.0, owner="test", overdraft_limit=50.0)
        transaction = acc.withdraw(75.0, "Overdraft withdrawal")
        self.assertAlmostEqual(acc.balance, -25.0)
        self.assertEqual(transaction.kind, "withdraw")
        self.assertEqual(transaction.amount, 75.0)
        self.assertEqual(len(acc.transactions), 1)

    def test_withdraw_overdraft_denied_current_account(self):
        acc = CurrentAccount(balance=50.0, owner="test", overdraft_limit=40.0)
        with self.assertRaises(ValueError) as ctx:
            acc.withdraw(100.0)
        self.assertIn("Insufficient funds", str(ctx.exception))

    def test_withdraw_invalid_amount_zero(self):
        acc = Account(balance=100.0, owner="test")
        with self.assertRaises(ValueError) as ctx:
            acc.withdraw(0.0)
        self.assertIn("must be positive", str(ctx.exception))

    def test_withdraw_invalid_amount_negative(self):
        acc = Account(balance=100.0, owner="test")
        with self.assertRaises(ValueError) as ctx:
            acc.withdraw(-10.0)
        self.assertIn("must be positive", str(ctx.exception))

    # Transfer Tests
    def test_transfer_updates_both(self):
        a = CurrentAccount(balance=200.0, owner="a")
        b = SavingsAccount(balance=50.0, owner="b")
        t_out, t_in = transfer(a, b, 75.0)
        self.assertAlmostEqual(a.balance, 125.0)
        self.assertAlmostEqual(b.balance, 125.0)
        self.assertEqual(t_out.kind, "transfer_out")
        self.assertEqual(t_in.kind, "transfer_in")
        self.assertEqual(len(a.transactions), 2)  # withdraw + transfer_out
        self.assertEqual(len(b.transactions), 2)  # deposit + transfer_in

    def test_transfer_insufficient_funds(self):
        a = Account(balance=50.0, owner="a")
        b = Account(balance=100.0, owner="b")
        with self.assertRaises(ValueError) as ctx:
            transfer(a, b, 75.0)
        self.assertIn("Insufficient funds", str(ctx.exception))

    def test_transfer_invalid_amount_zero(self):
        a = Account(balance=100.0, owner="a")
        b = Account(balance=100.0, owner="b")
        with self.assertRaises(ValueError) as ctx:
            transfer(a, b, 0.0)
        self.assertIn("must be positive", str(ctx.exception))

    def test_transfer_invalid_amount_negative(self):
        a = Account(balance=100.0, owner="a")
        b = Account(balance=100.0, owner="b")
        with self.assertRaises(ValueError) as ctx:
            transfer(a, b, -10.0)
        self.assertIn("must be positive", str(ctx.exception))

    def test_transfer_self(self):
        a = Account(balance=100.0, owner="a")
        with self.assertRaises(ValueError) as ctx:
            transfer(a, a, 50.0)
        self.assertIn("Cannot transfer to the same account", str(ctx.exception))

    # Interest Tests
    def test_interest_only_savings(self):
        s = SavingsAccount(balance=1000.0, owner="s", interest_rate=12.0)
        c = CurrentAccount(balance=1000.0, owner="c")
        transaction = s.apply_interest(months=1)
        # monthly rate = 12%/12 = 1% => interest = 10
        self.assertAlmostEqual(s.balance, 1010.0, places=2)
        self.assertEqual(transaction.kind, "interest")
        self.assertAlmostEqual(transaction.amount, 10.0, places=2)
        self.assertEqual(len(s.transactions), 1)
        # current account should not have an interest method
        with self.assertRaises(AttributeError):
            _ = c.apply_interest()

    def test_interest_zero_balance(self):
        s = SavingsAccount(balance=0.0, owner="s", interest_rate=12.0)
        transaction = s.apply_interest(months=1)
        self.assertIsNone(transaction)
        self.assertAlmostEqual(s.balance, 0.0)
        self.assertEqual(len(s.transactions), 0)

    def test_interest_multiple_months(self):
        s = SavingsAccount(balance=1000.0, owner="s", interest_rate=12.0)
        transaction = s.apply_interest(months=3)
        # monthly rate = 1% => interest = 10 * 3 = 30
        self.assertAlmostEqual(s.balance, 1030.0, places=2)
        self.assertEqual(transaction.kind, "interest")
        self.assertAlmostEqual(transaction.amount, 30.0, places=2)
        self.assertEqual(len(s.transactions), 1)

    def test_interest_invalid_months_zero(self):
        s = SavingsAccount(balance=1000.0, owner="s", interest_rate=12.0)
        transaction = s.apply_interest(months=0)
        self.assertIsNone(transaction)
        self.assertAlmostEqual(s.balance, 1000.0)
        self.assertEqual(len(s.transactions), 0)

    def test_interest_invalid_months_negative(self):
        s = SavingsAccount(balance=1000.0, owner="s", interest_rate=12.0)
        transaction = s.apply_interest(months=-1)
        self.assertIsNone(transaction)
        self.assertAlmostEqual(s.balance, 1000.0)
        self.assertEqual(len(s.transactions), 0)

if __name__ == '__main__':
    unittest.main()
