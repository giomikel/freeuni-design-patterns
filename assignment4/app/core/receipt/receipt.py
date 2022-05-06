from __future__ import annotations

import datetime
from abc import ABC, abstractmethod
from typing import List

from app.core.item import item


class AbstractReceipt(ABC):
    @abstractmethod
    def add(self, item_to_add: item.AbstractReceiptItem) -> None:
        pass

    @abstractmethod
    def get_sum(self) -> float:
        pass

    @abstractmethod
    def get_items(self) -> List[item.AbstractReceiptItem]:
        pass

    @abstractmethod
    def get_date(self) -> datetime.date:
        pass

    @abstractmethod
    def make_paid(self) -> None:
        pass

    @abstractmethod
    def is_paid(self) -> bool:
        pass


class Receipt(AbstractReceipt):
    def __init__(self) -> None:
        self._date = datetime.date.today()
        self._receipt_items: List[item.AbstractReceiptItem] = []
        self._sum: float = 0.0
        self._is_paid = False

    def add(self, item_to_add: item.AbstractReceiptItem) -> None:
        if not self._is_paid:
            self._receipt_items.append(item_to_add)
            self._sum += item_to_add.price

    def get_sum(self) -> float:
        return self._sum

    def get_items(self) -> List[item.AbstractReceiptItem]:
        return self._receipt_items

    def get_date(self) -> datetime.date:
        return self._date

    def make_paid(self) -> None:
        self._is_paid = True

    def is_paid(self) -> bool:
        return self._is_paid
