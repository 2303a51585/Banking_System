# TODO: Unit Testing for Withdraw, Transfer, and Interest

## Steps to Complete

1. **Update tests/test_accounts.py**:
   - Add comprehensive unit tests for `withdraw`:
     - Test normal withdrawal on base `Account` and `SavingsAccount`.
     - Test insufficient funds on base `Account`.
     - Test overdraft allowance and denial on `CurrentAccount`.
     - Test invalid amounts (negative or zero).
   - Add comprehensive unit tests for `transfer`:
     - Test normal transfer between accounts.
     - Test insufficient funds during transfer.
     - Test invalid transfer amounts (negative or zero).
     - Test self-transfer (if applicable).
   - Add comprehensive unit tests for `interest` (apply_interest on `SavingsAccount`):
     - Test normal interest application.
     - Test interest on zero balance.
     - Test interest over multiple months.
     - Test invalid months (negative or zero).
     - Ensure `CurrentAccount` does not have the `apply_interest` method.
   - Expand existing tests if necessary to cover more cases.

2. **Run the updated tests**:
   - Execute `python -m unittest tests/test_accounts.py` to verify all tests pass.
   - If any tests fail, debug and fix issues in `models.py` or the tests.

## Progress Tracking
- [x] Step 1: Update tests/test_accounts.py
- [x] Step 2: Run tests and verify
