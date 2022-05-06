from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict

from app.core.item import item
from app.core.receipt import receipt
from app.core.receipt.receipt import AbstractReceipt


class AbstractCashier(ABC):
    @abstractmethod
    def open_receipt(self) -> bool:
        pass

    @abstractmethod
    def add(self, item_to_add: item.AbstractReceiptItem) -> receipt.AbstractReceipt:
        pass

    @abstractmethod
    def close_paid_receipt(self, paid: bool) -> bool:
        pass

    @abstractmethod
    def get_receipt(self) -> receipt.AbstractReceipt:
        pass


class Cashier(AbstractCashier):  # Receipt Builder
    def __init__(self) -> None:
        self._is_closed = False
        self._receipt = receipt.Receipt()

    def open_receipt(self) -> bool:  # Reset
        if self._is_closed:
            self._receipt = receipt.Receipt()
            self._is_closed = False
            return True
        else:
            return False

    def add(self, item_to_add: item.AbstractReceiptItem) -> receipt.AbstractReceipt:
        self._receipt.add(item_to_add)
        return self._receipt

    def close_paid_receipt(self, paid: bool) -> bool:
        if paid and not self._is_closed:
            self._receipt.make_paid()
            self._is_closed = True
            return True
        else:
            return False

    def get_receipt(self) -> receipt.AbstractReceipt:
        return self._receipt


class XReport:
    def __init__(self) -> None:
        self._register: Dict[str, int] = {}
        self._total_revenue: float = 0.0
        self._closed_receipt_count: int = 0

    def add_receipt_to_report(self, receipt_to_add: AbstractReceipt) -> None:
        for itm in receipt_to_add.get_items():
            if itm.get_name() in self._register:
                self._register[itm.get_name()] += 1
            else:
                self._register[itm.get_name()] = 1
        self._total_revenue += receipt_to_add.get_sum()
        self._closed_receipt_count += 1

    def get_report(self) -> Dict[str, int]:
        return self._register

    def get_revenue(self) -> float:
        return self._total_revenue

    def get_closed_receipt_count(self) -> int:
        return self._closed_receipt_count
