from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from app.core.customer.customer_interactor import (
    CustomerInteractor,
    FetchReceiptResponse,
    PaymentRequest,
    PaymentResponse,
)
from app.core.store.cashier_interactor import (
    AddItemRequest,
    AddItemResponse,
    CashierInteractor,
    ErrorResponse,
    ItemRepository,
    ReceiptRepository,
    ResultReceiptResponse,
)
from app.core.store.manager_interactor import (
    ManagerInteractor,
    XReportRequest,
    XReportResponse,
)
from app.core.store.store import AbstractCashier


@dataclass
class CustomerService:
    customer_interactor: CustomerInteractor

    def fetch_receipt(self) -> Union[FetchReceiptResponse, ResultReceiptResponse]:
        return self.customer_interactor.fetch_receipt()

    def pay(self, request: PaymentRequest) -> PaymentResponse:
        return self.customer_interactor.pay(request)

    @classmethod
    def create(cls, cashier: AbstractCashier) -> CustomerService:
        return cls(customer_interactor=CustomerInteractor(cashier))


@dataclass
class CashierService:
    cashier_interactor: CashierInteractor

    def open_receipt(self) -> ResultReceiptResponse:
        return self.cashier_interactor.open_receipt()

    def add_item(
        self, request: AddItemRequest
    ) -> Union[AddItemResponse, ErrorResponse]:
        return self.cashier_interactor.add_item(request)

    def close_receipt(self) -> ResultReceiptResponse:
        return self.cashier_interactor.close_receipt()

    @classmethod
    def create(
        cls,
        cashier: AbstractCashier,
        item_repository: ItemRepository,
        receipt_repository: ReceiptRepository,
    ) -> CashierService:
        return cls(
            cashier_interactor=CashierInteractor(
                cashier, item_repository, receipt_repository
            )
        )


@dataclass
class ManagerService:
    manager_interactor: ManagerInteractor

    def make_x_report(self, request: XReportRequest) -> XReportResponse:
        return self.manager_interactor.make_x_report(request)

    @classmethod
    def create(cls, receipt_repository: ReceiptRepository) -> ManagerService:
        return cls(manager_interactor=ManagerInteractor(receipt_repository))
