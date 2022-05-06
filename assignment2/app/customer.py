from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from app import item, receipt


class AbstractCustomer(ABC):
    @abstractmethod
    def see_receipt(self, receipt_: receipt.AbstractReceipt) -> None:
        pass

    @abstractmethod
    def make_payment(self) -> bool:
        pass

    @abstractmethod
    def get_items(self) -> List[item.AbstractReceiptItem]:
        pass


class Customer(AbstractCustomer):
    def __init__(
        self, items: List[item.AbstractReceiptItem], payment_strategy: Payment
    ):
        self._items = items
        self._payment_strategy = payment_strategy

    def see_receipt(self, receipt_: receipt.AbstractReceipt) -> None:
        self._receipt = receipt_

    def make_payment(self) -> bool:
        return self._payment_strategy.pay()

    def get_items(self) -> List[item.AbstractReceiptItem]:
        return self._items


class Payment(ABC):
    @abstractmethod
    def pay(self) -> bool:
        pass


class CardPayment(Payment):
    def pay(self) -> bool:
        print("Payment: Customer paid with card\n")
        return True


class CashPayment(Payment):
    def pay(self) -> bool:
        print("Payment: Customer paid with cash\n")
        return True
