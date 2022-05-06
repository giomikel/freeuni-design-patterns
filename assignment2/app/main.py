import random
from typing import List

from app import customer, item, store


class Driver:
    def __init__(self, items: List[item.AbstractReceiptItem]) -> None:
        self._item_list = items
        self._x_report = store.XReport()
        self._cashier = store.Cashier(self._x_report)
        self._manager = store.StoreManager(self._x_report)
        self._strategies = [customer.CardPayment, customer.CashPayment]
        self._count = 0
        self._shift_active = True

    def simulate_shift(self) -> None:
        while self._shift_active:
            random_payment_strategy = random.choice(self._strategies)
            cst = customer.Customer(
                random.sample(item_list, random.randint(1, len(item_list))),
                random_payment_strategy(),
            )
            self._cashier.open_receipt()
            receipt = self._cashier.add_item_list(cst.get_items())
            receipt.receipt()
            cst.see_receipt(receipt)
            self._cashier.close_paid_receipt(cst.make_payment())
            self._count += 1
            self._x_report_prompt()
            self._z_report_prompt()

    def _x_report_prompt(self) -> None:
        if self._count % 20 == 0:
            print("Prompt to Manager: Do you want to make x report?")
            if random.choice([True, False]):
                print("Manager: Yes\n")
                self._manager.make_x_report()
            else:
                print("Manager: No\n")

    def _z_report_prompt(self) -> None:
        if self._count % 100 == 0:
            print("Prompt to Manager: Do you want to end the shift?")
            if random.choice([True, False]):
                print("Manager: Yes\n")
                self._cashier.make_z_report()
                self._shift_active = False
            else:
                print("Manager: No\n")


if __name__ == "__main__":
    it1 = item.Item("Water", 0.5, 0)
    it2 = item.Item("Milk", 2.0, 0)
    it3 = item.Item("Bread", 1.0, 0)
    it4 = item.Item("Beer", 2.3, 0)
    it5 = item.Item("Chips", 2.5, 0)
    it6 = item.CompositeItem("Water Pack", [it1, it1, it1], 0.1)
    it7 = item.CompositeItem("Beer Combo", [it4, it5], 0.15, is_combo=True)
    item_list = [it1, it2, it3, it4, it5, it6, it7]
    driver = Driver(item_list)
    driver.simulate_shift()
