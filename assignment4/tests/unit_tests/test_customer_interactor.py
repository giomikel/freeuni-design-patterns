import pytest

from app.core.customer import customer_interactor
from app.core.customer.customer_interactor import (
    FetchReceiptResponse,
    PaymentRequest,
    PaymentResponse,
)
from app.core.item.item import Item
from app.core.store.cashier_interactor import AddItemResponse
from app.core.store.store import Cashier


@pytest.fixture
def ci() -> customer_interactor.CustomerInteractor:
    cashier = Cashier()
    itm = Item("Milk", 2.2)
    cashier.add(itm)
    return customer_interactor.CustomerInteractor(cashier)


def test_customer_interactor_fetch_receipt(
    ci: customer_interactor.CustomerInteractor,
) -> None:
    assert ci.fetch_receipt() == FetchReceiptResponse(
        [AddItemResponse("Milk", 1, 2.2, 2.2)], 2.2
    )


def test_customer_get_items(ci: customer_interactor.CustomerInteractor) -> None:
    assert ci.pay(PaymentRequest(2.1)) == PaymentResponse(False, "Insufficient amount")
    assert ci.pay(PaymentRequest(2.3)) == PaymentResponse(True, "Successful payment")
