import pytest

from app import item
from app import receipt as receipt_file


@pytest.fixture
def receipt() -> receipt_file.AbstractReceipt:
    rcpt = receipt_file.Receipt()
    it = item.Item("Milk", 2.2)
    rcpt.add(it)
    return rcpt


def test_receipt_add_remove(receipt: receipt_file.AbstractReceipt) -> None:
    it = item.Item("Water", 1.0)
    receipt.add(it)
    assert len(receipt.get_items()) == 2
    receipt.remove(it)
    assert len(receipt.get_items()) == 1


def test_receipt_get_sum(receipt: receipt_file.AbstractReceipt) -> None:
    assert receipt.get_sum() == 2.2


def test_receipt_get_items(receipt: receipt_file.AbstractReceipt) -> None:
    assert isinstance(receipt.get_items(), list) is True
    assert isinstance(receipt.get_items()[0], item.AbstractReceiptItem)
