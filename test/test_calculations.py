import pytest
from app.calculations import add, BankAccount


@pytest.mark.parametrize("num1,num2,result", [(2, 3, 5), (3, 4, 7), (23, 43, 66)])
def test_add(num1, num2, result):
    print("testing add function")
    assert add(num1, num2) == result


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


def test_bank_set_initial_amount():
    bank_account = BankAccount(50)
    assert bank_account.balance == 50


def test_bank_default_amount():
    bank_account = BankAccount()
    assert bank_account.balance == 0


def test_deposit():
    bank_account = BankAccount(55)
    bank_account.deposit(56)
    assert bank_account.balance == 111


@pytest.mark.parametrize("deposited, withdrew, result", [(500, 200, 300), (450, 250, 200), (333, 222, 111)])
def test_bank_transaction(zero_bank_account, deposited, withdrew, result):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == result
