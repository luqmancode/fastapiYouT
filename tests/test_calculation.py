import pytest
from app import calculation as cal

@pytest.fixture
def zero_bank_account():
    return cal.BankAccount()

@pytest.fixture
def hundred_balance_account():
    return cal.BankAccount(100)

@pytest.mark.parametrize("num1, num2, expected", [(2, 4, 6), (-1, -2, -3), (4, 5, 9), (9.5, 2.5, 12)])
def test_add(num1, num2, expected):
    assert cal.add(num1, num2) == expected, "Addition is not performing"

@pytest.mark.parametrize("num1, num2, expected", [(-1, 10, -11), (2, 1, 1), (3, 4, -1), (6.5, 4.5, 2)])
def test_sub(num1, num2, expected):
    assert cal.sub(num1, num2) == expected, "Subtraction has error"

def test_mul():
    assert cal.mul(10, 2) == 20, "Multiplication has error"

def test_div():
    assert cal.div(4, 2) == 2, "Division has error"


def test_with_default_balance(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_with_opening_balance_account(hundred_balance_account):
    # bank_account = cal.BankAccount(100) after pytest fixture
    assert hundred_balance_account.balance == 100

def test_deposit():
    bank_account = cal.BankAccount(100)
    bank_account.deposit(50)
    assert bank_account.balance == 150

def test_withdraw():
    bank_account = cal.BankAccount(100)
    bank_account.withdraw(20) 
    assert bank_account.balance == 80

def test_interest():
    bank_account = cal.BankAccount(100)
    bank_account.add_interest()
    assert round(bank_account.balance, 6) == 110

# parametrize with fixture in one test
@pytest.mark.parametrize("deposited, withdrew, expected", [(900, 400, 600), (100, 100, 100)])
def test_with_transaction(hundred_balance_account, deposited, withdrew, expected):
    hundred_balance_account.deposit(deposited)
    hundred_balance_account.withdraw(withdrew)
    assert hundred_balance_account.balance == expected

# exception test case passing
def test_with_excess_withdraw(zero_bank_account):
    with pytest.raises(Exception):  # passed here  cal.InsufficientFundException is also pass here due to base class
        assert zero_bank_account.withdraw(100)

def test_with_zero_withdraw(zero_bank_account):
    # with pytest.raises(cal.InsufficientFundException):  # passed
    #     assert zero_bank_account.withdraw(0)

    with pytest.raises(cal.InsufficientFundException):
        assert zero_bank_account.withdraw(0)