from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional


class AbstractReceiptItem(ABC):
    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, price: float) -> None:
        self._price = price

    @abstractmethod
    def get_amount(self) -> int:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_unit_price(self) -> float:
        pass

    def __str__(self) -> str:
        return (
            self.get_name()
            + " "
            + str(self.get_amount())
            + " "
            + "{:.2f}".format(self.get_unit_price())
            + " "
            + "{:.2f}".format(self.price)
        )

    def __hash__(self) -> int:
        return hash(self.get_name())


class Item(AbstractReceiptItem):
    def __init__(self, name: str, price: float) -> None:
        self._name = name
        self._price = price

    def get_amount(self) -> int:
        return 1

    def get_name(self) -> str:
        return self._name

    def get_unit_price(self) -> float:
        return self._price


class CompositeItem(AbstractReceiptItem):
    def __init__(
        self, name: str, items: Optional[List[AbstractReceiptItem]] = None
    ) -> None:
        self._name = name
        self._children: List[AbstractReceiptItem] = [] if items is None else items
        self._units = len(self._children)
        self._update_total()

    def add(self, item: AbstractReceiptItem) -> None:
        self._children.append(item)
        self._units += 1
        self._update_total()

    def remove(self, item: AbstractReceiptItem) -> None:
        if item in self._children:
            self._children.remove(item)
            self._units -= 1
            self._update_total()

    def get_amount(self) -> int:
        return self._units

    def get_name(self) -> str:
        return self._name

    def get_items(self) -> List[AbstractReceiptItem]:
        return [child for child in self._children]

    def get_unit_price(self) -> float:
        return self._unit_price

    def _update_total(self) -> None:
        result = 0.0
        for child in self._children:
            result += child.price
        self.price = result
        self._unit_price = result / self._units if self._children else 0
