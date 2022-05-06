import datetime
from dataclasses import dataclass
from typing import List, Optional, Protocol, Union

from app.core.item.item import AbstractReceiptItem
from app.core.receipt.receipt import AbstractReceipt
from app.core.store.store import AbstractCashier


@dataclass
class ResultReceiptResponse:
    success: bool
    message: str


@dataclass
class AddItemRequest:
    item_name: str


@dataclass
class AddItemResponse:
    item_name: str
    units: int
    unit_price: float
    total_price: float


@dataclass
class ErrorResponse:
    message: str


class ItemRepository(Protocol):
    def create_item(self, item: AbstractReceiptItem) -> None:
        pass

    def get_item(self, item_name: str) -> Optional[AbstractReceiptItem]:
        pass


class ReceiptRepository(Protocol):
    def write_receipt(self, receipt: AbstractReceipt) -> None:
        pass

    def get_receipts_from_date(self, date: datetime.date) -> List[AbstractReceipt]:
        pass


@dataclass
class CashierInteractor:
    cashier: AbstractCashier
    item_repository: ItemRepository
    receipt_repository: ReceiptRepository

    """
    Receipt is open by default on run
    """

    def open_receipt(self) -> ResultReceiptResponse:
        successful_open = self.cashier.open_receipt()
        message = (
            "Operation Successful" if successful_open else "Close current receipt first"
        )
        return ResultReceiptResponse(successful_open, message)

    def add_item(
        self, request: AddItemRequest
    ) -> Union[AddItemResponse, ErrorResponse]:
        item = self.item_repository.get_item(request.item_name)
        if item:
            self.cashier.add(item)
            return AddItemResponse(
                item.get_name(), item.get_amount(), item.get_unit_price(), item.price
            )
        return ErrorResponse("Error: Item doesn't exist")

    def close_receipt(self) -> ResultReceiptResponse:
        is_closed = self.cashier.close_paid_receipt(
            self.cashier.get_receipt().is_paid()
        )
        message = "Receipt closed"
        if is_closed:
            self.receipt_repository.write_receipt(self.cashier.get_receipt())
        else:
            message = "Receipt not paid for"
        return ResultReceiptResponse(is_closed, message)
