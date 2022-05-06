from typing import Union

from fastapi import APIRouter, Depends

from app.core.customer.customer_interactor import (
    FetchReceiptResponse,
    PaymentRequest,
    PaymentResponse,
)
from app.core.facade import CustomerService
from app.core.store.cashier_interactor import ResultReceiptResponse
from app.infra.fastapi.dependables import get_core_customer

customer_api = APIRouter()


@customer_api.get("/customer/receipt")
def fetch_receipt(
    core: CustomerService = Depends(get_core_customer),
) -> Union[FetchReceiptResponse, ResultReceiptResponse]:
    return core.fetch_receipt()


@customer_api.post("/customer/payment={amount}")
def pay(
    amount: str, core: CustomerService = Depends(get_core_customer)
) -> PaymentResponse:
    return core.pay(PaymentRequest(float(amount)))
