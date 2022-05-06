from typing import Union

from fastapi import APIRouter, Depends

from app.core.facade import CashierService
from app.core.store.cashier_interactor import (
    AddItemRequest,
    AddItemResponse,
    ErrorResponse,
    ResultReceiptResponse,
)
from app.infra.fastapi.dependables import get_core_cashier

cashier_api = APIRouter()


@cashier_api.post("/cashier/open")
def open_receipt(
    core: CashierService = Depends(get_core_cashier),
) -> ResultReceiptResponse:
    return core.open_receipt()


@cashier_api.post("/cashier/add_item={item_name}")
def add_item(
    item_name: str, core: CashierService = Depends(get_core_cashier)
) -> Union[AddItemResponse, ErrorResponse]:
    return core.add_item(AddItemRequest(item_name))


@cashier_api.post("/cashier/close_receipt")
def close_receipt(
    core: CashierService = Depends(get_core_cashier),
) -> ResultReceiptResponse:
    return core.close_receipt()
