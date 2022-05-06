from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from app import item


class AbstractReceipt(ABC):
    @abstractmethod
    def receipt(self) -> None:
        pass

    @abstractmethod
    def add(self, item_to_add: item.AbstractReceiptItem) -> None:
        pass

    @abstractmethod
    def remove(self, item_to_remove: item.AbstractReceiptItem) -> None:
        pass

    @abstractmethod
    def get_sum(self) -> float:
        pass

    @abstractmethod
    def get_items(self) -> List[item.AbstractReceiptItem]:
        pass


class Receipt(AbstractReceipt):
    def __init__(self) -> None:
        self._receipt_items: List[item.AbstractReceiptItem] = []
        self._sum: float = 0.0

    def receipt(self) -> None:
        print("Name|Units|Price|Total\n----------------------")
        for itm in self._receipt_items:
            print(itm)
        print("\nSum: {:.2f}".format(self._sum))

    def add(self, item_to_add: item.AbstractReceiptItem) -> None:
        self._receipt_items.append(item_to_add)
        self._sum += item_to_add.price

    def remove(self, item_to_remove: item.AbstractReceiptItem) -> None:
        if item_to_remove in self._receipt_items:
            self._receipt_items.remove(item_to_remove)
            self._sum -= item_to_remove.price

    def get_sum(self) -> float:
        return self._sum

    def get_items(self) -> List[item.AbstractReceiptItem]:
        return self._receipt_items
