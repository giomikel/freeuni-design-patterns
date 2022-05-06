from dataclasses import dataclass
from typing import List, Union

from app.core.store.cashier_interactor import AddItemResponse, ResultReceiptResponse
from app.core.store.store import AbstractCashier


@dataclass
class FetchReceiptResponse:
    items: List[AddItemResponse]
    grand_total: float


@dataclass
class PaymentRequest:
    amount: float


@dataclass
class PaymentResponse:
    success: bool
    message: str


@dataclass
class CustomerInteractor:
    cashier: AbstractCashier

    def fetch_receipt(self) -> Union[FetchReceiptResponse, ResultReceiptResponse]:
        receipt = self.cashier.get_receipt()
        item_list = []
        for itm in receipt.get_items():
            item_list.append(
                AddItemResponse(
                    itm.get_name(), itm.get_amount(), itm.get_unit_price(), itm.price
                )
            )
        return FetchReceiptResponse(item_list, receipt.get_sum())

    """
    ცარიელი ჩეკის გადახდა გამიზნულად დავტოვე, იქნებ გადაიფიქროს კლიენტმა ყიდვა,
    მაგ შემთხვევაში payment-ის ველში შევიყვანთ დადებით მნიშვნელობას და დავხურავთ ჩეკს
    ცარიელი ჩეკი ბაზაში არ აისახება
    """

    def pay(self, request: PaymentRequest) -> PaymentResponse:
        receipt = self.cashier.get_receipt()
        message = "Insufficient amount"
        receipt_sum = receipt.get_sum()
        is_sufficient = receipt_sum <= request.amount
        if receipt.is_paid():
            message = "Already paid"
        elif is_sufficient:
            receipt.make_paid()
            message = "Successful payment"
        return PaymentResponse(receipt.is_paid(), message)
