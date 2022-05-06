import datetime

import pytest

from app.core.item import item
from app.core.receipt import receipt as receipt_file


@pytest.fixture
def receipt() -> receipt_file.AbstractReceipt:
    rcpt = receipt_file.Receipt()
    it = item.Item("Milk", 2.2)
    rcpt.add(it)
    return rcpt


def test_receipt_add(receipt: receipt_file.AbstractReceipt) -> None:
    it = item.Item("Water", 1.0)
    receipt.add(it)
    assert len(receipt.get_items()) == 2


def test_receipt_get_sum(receipt: receipt_file.AbstractReceipt) -> None:
    assert receipt.get_sum() == 2.2


def test_receipt_get_items(receipt: receipt_file.AbstractReceipt) -> None:
    assert isinstance(receipt.get_items(), list) is True
    assert isinstance(receipt.get_items()[0], item.AbstractReceiptItem)


def test_receipt_get_date(receipt: receipt_file.AbstractReceipt) -> None:
    assert receipt.get_date() == datetime.date.today()


def test_receipt_make_paid_is_paid(receipt: receipt_file.AbstractReceipt) -> None:
    assert receipt.is_paid() is False
    receipt.make_paid()
    assert receipt.is_paid() is True
