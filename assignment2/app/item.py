from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional


class AbstractReceiptItem(ABC):
    @abstractmethod
    def is_composite(self) -> bool:
        pass

    @abstractmethod
    def get_discount(self) -> float:
        pass

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


class Item(AbstractReceiptItem):
    def __init__(self, name: str, price: float, discount: float = 0) -> None:
        self._name = name
        self._price = price * (1 - discount)
        self._discount = discount

    def is_composite(self) -> bool:
        return False

    def get_amount(self) -> int:
        return 1

    def get_discount(self) -> float:
        return self._discount

    def get_name(self) -> str:
        return self._name

    def get_unit_price(self) -> float:
        return self._price

    def __str__(self) -> str:
        return (
            self._name
            + " "
            + str(self.get_amount())
            + " "
            + "{:.2f}".format(self.get_unit_price())
            + " "
            + "{:.2f}".format(self.price)
        )


class CompositeItem(AbstractReceiptItem):
    def __init__(
        self,
        name: str,
        items: Optional[List[AbstractReceiptItem]] = None,
        discount: float = 0,
        is_combo: bool = False,
    ) -> None:
        self._name = name
        self._discount = discount
        self._children: List[AbstractReceiptItem] = [] if items is None else items
        self._units = len(self._children)
        self._is_combo = is_combo
        self._update_total()

    def add(self, item: AbstractReceiptItem) -> None:
        if item not in self._children:
            self._is_combo = True
        self._children.append(item)
        item.price *= 1 - self._discount
        self._units += 1
        self._update_total()

    def remove(self, item: AbstractReceiptItem) -> None:
        if item in self._children:
            self._children.remove(item)
            self._units -= 1
            self._update_total()

    def is_composite(self) -> bool:
        return True

    def get_amount(self) -> int:
        return self._units

    def get_discount(self) -> float:
        return self._discount

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
        self.price = result * (1 - self._discount)
        self._unit_price = result / self._units if self._is_combo is False else 0

    def __str__(self) -> str:
        res = ""
        if self._is_combo:
            lst = self.get_items()
            res += "--\n"
            for itm in lst:
                res += (
                    itm.get_name()
                    + " "
                    + str(itm.get_amount())
                    + " "
                    + "{:.2f}".format(itm.get_unit_price())
                    + " "
                    + "{:.2f}".format(itm.price)
                    + "\n"
                )
            res += (
                "--Combination Price: "
                + str(self.price)
                + " Discount: "
                + str(self._discount * 100)
                + "%"
            )
        else:
            res += (
                self.get_name()
                + " "
                + str(self.get_amount())
                + " "
                + "{:.2f}".format(self.get_unit_price())
                + " "
                + "{:.2f}".format(self.price)
            )
        return res
