import datetime

from app.core.item.item import Item
from app.core.receipt.receipt import Receipt
from app.infra.in_memory.item_in_memory import ItemInMemoryRepository
from app.infra.in_memory.receipt_in_memory import ReceiptInMemoryRepository


def test_item_repository_create_and_get_item() -> None:
    repository = ItemInMemoryRepository()
    milk = Item("Milk", 2.2)
    soda = Item("Soda", 1.2)
    assert repository.get_item("Milk") is None
    assert repository.get_item("Soda") is None
    repository.create_item(milk)
    repository.create_item(soda)
    assert repository.get_item("Milk") == milk
    assert repository.get_item("Soda") == soda
    assert repository.get_item("Water") is None


def test_receipt_repository_write_and_get_receipts() -> None:
    repository = ReceiptInMemoryRepository()
    receipt = Receipt()
    milk = Item("Milk", 2.2)
    receipt.add(milk)
    assert repository.get_receipts_from_date(datetime.date.today()) == []
    repository.write_receipt(receipt)
    assert len(repository.get_receipts_from_date(datetime.date.today())) > 0
    assert repository.get_receipts_from_date(datetime.date.today()) == [receipt]
