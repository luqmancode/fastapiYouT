# to learn pytest only

def add(num1: float, num2: float):
    return num1 + num2

def sub(num1: float, num2: float):
    return num1 - num2

def mul(num1: float, num2: float):
    return num1 * num2

def div(num1: float, num2: float):
    return num1 / num2

class InsufficientFundException(Exception):
    pass

class BankAccount:
    def __init__(self, starting_balance = 0):
        self.balance = starting_balance

    def deposit(self, value):
        assert value >= 0, f"value {value} should not be negative value"
        self.balance += value
        return self.balance

    def withdraw(self, value):
        assert value >= 0, f"value {value} should not be negative value"
        if value == 0:
            raise InsufficientFundException("Specific exception is caught")
            # raise ZeroDivisionError() # this cause exception error in code as expected different
        if value > self.balance:
            raise Exception(f"Withdraw {value} becomes insufficient funds in account")
        self.balance -= value

    def add_interest(self):
        self.balance *= 1.1  # 1 percent of interest

