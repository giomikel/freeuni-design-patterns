from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List

from app import item, receipt

# class AbstractEmployee(ABC): ---Would probably violate interface segregation principle
#
#     @abstractmethod
#     def make_report(self):
#         pass


class AbstractCashier(ABC):
    @abstractmethod
    def open_receipt(self) -> None:
        pass

    @abstractmethod
    def add(self, item_to_add: item.AbstractReceiptItem) -> receipt.AbstractReceipt:
        pass

    @abstractmethod
    def add_item_list(
        self, items: List[item.AbstractReceiptItem]
    ) -> receipt.AbstractReceipt:
        pass

    @abstractmethod
    def remove(
        self, item_to_remove: item.AbstractReceiptItem
    ) -> receipt.AbstractReceipt:
        pass

    @abstractmethod
    def close_paid_receipt(self, paid: bool) -> None:
        pass

    @abstractmethod
    def make_z_report(self) -> None:
        pass


class Cashier(AbstractCashier):  # Receipt Builder
    def __init__(self, x_report: XReport) -> None:
        self.open_receipt()
        self._x_report = x_report

    def open_receipt(self) -> None:  # Reset
        self._receipt = receipt.Receipt()

    def add(self, item_to_add: item.AbstractReceiptItem) -> receipt.AbstractReceipt:
        self._receipt.add(item_to_add)
        self._x_report.add_to_report(item_to_add)
        return self._receipt

    def add_item_list(
        self, items: List[item.AbstractReceiptItem]
    ) -> receipt.AbstractReceipt:
        for itm in items:
            self._receipt.add(itm)
            self._x_report.add_to_report(itm)
        return self._receipt

    def remove(
        self, item_to_remove: item.AbstractReceiptItem
    ) -> receipt.AbstractReceipt:
        if item_to_remove in self._receipt.get_items():
            self._receipt.remove(item_to_remove)
            self._x_report.remove_from_report(item_to_remove)
        return self._receipt

    def close_paid_receipt(self, paid: bool) -> None:
        if paid:
            self.open_receipt()
        else:
            print("Payment Declined")

    def make_z_report(self) -> None:
        ZReport.clear_register(self._x_report)


class AbstractStoreManager(ABC):
    @abstractmethod
    def make_x_report(self) -> None:
        pass


class StoreManager(AbstractStoreManager):
    def __init__(self, x_report: XReport) -> None:
        self._x_report = x_report

    def make_x_report(self) -> None:
        print("Name|Sold\n---------")
        for itm in self._x_report.get_report():
            print(itm.get_name(), self._x_report.get_report()[itm])
        print("\nTotal Revenue: {:.2f}".format(self._x_report.get_revenue()))


class XReport:
    def __init__(self) -> None:
        self.reset()

    def add_to_report(self, item_to_add: item.AbstractReceiptItem) -> None:
        if item_to_add in self._register:
            self._register[item_to_add] += 1
        else:
            self._register[item_to_add] = 1
        self._total_revenue += item_to_add.price

    def remove_from_report(self, item_to_remove: item.AbstractReceiptItem) -> None:
        if item_to_remove in self._register:
            if self._register[item_to_remove] == 1:
                self._register.pop(item_to_remove)
            else:
                self._register[item_to_remove] -= 1
            self._total_revenue -= item_to_remove.price

    def get_report(self) -> Dict[item.AbstractReceiptItem, int]:
        return self._register

    def get_revenue(self) -> float:
        return self._total_revenue

    def reset(self) -> None:
        self._register: Dict[item.AbstractReceiptItem, int] = {}
        self._total_revenue: float = 0.0


class ZReport:
    @staticmethod
    def clear_register(x_report: XReport) -> None:
        x_report.reset()
