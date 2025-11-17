import unittest
from account import SavingsAccount, CurrentAccount

class TestBankSystem(unittest.TestCase):

    def setUp(self):
        self.savings = SavingsAccount("S101", "Alice", 1000, interest_rate=0.10)
        self.current = CurrentAccount("C202", "Bob", 500)

    def test_insufficient_balance(self):
        with self.assertRaises(ValueError):
            self.current.withdraw(600)

    def test_transfer(self):
        self.savings.transfer(self.current, 200)
        self.assertEqual(self.savings.balance, 800)
        self.assertEqual(self.current.balance, 700)

    def test_interest(self):
        interest = self.savings.apply_interest()
        self.assertEqual(interest, 100)
        self.assertEqual(self.savings.balance, 1100)
        with self.assertRaises(AttributeError):
            self.current.apply_interest()

if __name__ == '__main__':
    unittest.main()

