import datetime
from typing import Tuple

import pytest

from app.core.item.item import Item
from app.core.receipt.receipt import Receipt
from app.core.store import cashier_interactor, manager_interactor
from app.core.store.cashier_interactor import (
    AddItemRequest,
    AddItemResponse,
    ErrorResponse,
    ResultReceiptResponse,
)
from app.core.store.manager_interactor import XReportRequest, XReportResponse
from app.core.store.store import AbstractCashier, Cashier
from app.infra.in_memory.item_in_memory import ItemInMemoryRepository
from app.infra.in_memory.receipt_in_memory import ReceiptInMemoryRepository


@pytest.fixture
def ci() -> Tuple[AbstractCashier, cashier_interactor.CashierInteractor]:
    cashier = Cashier()
    item_repository = ItemInMemoryRepository()
    item_repository.create_item(Item("Milk", 2.2))
    receipt_repository = ReceiptInMemoryRepository()
    interactor = cashier_interactor.CashierInteractor(
        cashier, item_repository, receipt_repository
    )
    return cashier, interactor


def test_cashier_interactor_open_receipt(
    ci: Tuple[AbstractCashier, cashier_interactor.CashierInteractor]
) -> None:
    cashier = ci[0]
    interactor = ci[1]
    assert interactor.open_receipt() == ResultReceiptResponse(
        False, "Close current receipt first"
    )
    cashier.get_receipt().make_paid()
    interactor.close_receipt()
    assert interactor.open_receipt() == ResultReceiptResponse(
        True, "Operation Successful"
    )


def test_cashier_interactor_add_item(
    ci: Tuple[AbstractCashier, cashier_interactor.CashierInteractor]
) -> None:
    cashier = ci[0]
    interactor = ci[1]
    assert len(cashier.get_receipt().get_items()) == 0
    assert interactor.add_item(AddItemRequest("Milk")) == AddItemResponse(
        "Milk", 1, 2.2, 2.2
    )
    assert interactor.add_item(AddItemRequest("Wotah")) == ErrorResponse(
        "Error: Item doesn't exist"
    )
    assert len(cashier.get_receipt().get_items()) == 1


def test_cashier_interactor_close_receipt(
    ci: Tuple[AbstractCashier, cashier_interactor.CashierInteractor]
) -> None:
    cashier = ci[0]
    interactor = ci[1]
    assert interactor.close_receipt() == ResultReceiptResponse(
        False, "Receipt not paid for"
    )
    cashier.get_receipt().make_paid()
    assert interactor.close_receipt() == ResultReceiptResponse(True, "Receipt closed")


@pytest.fixture
def mi() -> Tuple[ReceiptInMemoryRepository, manager_interactor.ManagerInteractor]:
    receipt_repository = ReceiptInMemoryRepository()
    interactor = manager_interactor.ManagerInteractor(receipt_repository)
    return receipt_repository, interactor


def test_manager_interactor_make_x_report(
    mi: Tuple[ReceiptInMemoryRepository, manager_interactor.ManagerInteractor]
) -> None:
    repository = mi[0]
    interactor = mi[1]
    assert interactor.make_x_report(
        XReportRequest(datetime.date.today())
    ) == XReportResponse(0, {}, 0)
    receipt = Receipt()
    receipt.add(Item("Milk", 2.2))
    repository.write_receipt(receipt)
    assert interactor.make_x_report(
        XReportRequest(datetime.date.today())
    ) == XReportResponse(2.2, {"Milk": 1}, 1)
