from fastapi import FastAPI

from app.core.facade import CashierService, CustomerService, ManagerService
from app.core.item.item import CompositeItem, Item
from app.core.store.cashier_interactor import ItemRepository
from app.core.store.store import Cashier
from app.infra.fastapi.cashier_router import cashier_api
from app.infra.fastapi.customer_router import customer_api
from app.infra.fastapi.manager_router import manager_api
from app.infra.sqlite.item_sqlite import ItemSqlite
from app.infra.sqlite.receipt_sqlite import ReceiptSqlite


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(customer_api)
    app.include_router(cashier_api)
    app.include_router(manager_api)
    cashier = Cashier()
    item_repository = setup_item_repository()
    receipt_repository = ReceiptSqlite()
    app.state.customer = CustomerService.create(cashier)
    app.state.cashier = CashierService.create(
        cashier, item_repository, receipt_repository
    )
    app.state.manager = ManagerService.create(receipt_repository)
    return app


def setup_item_repository() -> ItemRepository:
    item_repository = ItemSqlite()
    item1 = Item("Milk", 2.2)
    item2 = Item("Water", 0.7)
    item3 = Item("Cheese", 3.4)
    item4 = CompositeItem("Water 3-Pack", [item2, item2, item2])
    item_repository.create_item(item1)
    item_repository.create_item(item2)
    item_repository.create_item(item3)
    item_repository.create_item(item4)
    return item_repository
