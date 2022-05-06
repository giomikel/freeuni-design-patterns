import random

import pytest

from app import customer as customer_file
from app import item


@pytest.fixture
def customer() -> customer_file.Customer:
    it = item.Item("Milk", 2.2)
    strategy = random.choice([customer_file.CardPayment, customer_file.CashPayment])
    payment_strategy = strategy()
    return customer_file.Customer([it], payment_strategy)


def test_customer_make_payment(customer: customer_file.Customer) -> None:
    assert customer.make_payment() is True


def test_customer_get_items(customer: customer_file.Customer) -> None:
    assert len(customer.get_items()) == 1
