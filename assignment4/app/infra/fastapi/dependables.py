from typing import Any

from starlette.requests import Request


def get_core_customer(request: Request) -> Any:
    return request.app.state.customer


def get_core_cashier(request: Request) -> Any:
    return request.app.state.cashier


def get_core_manager(request: Request) -> Any:
    return request.app.state.manager
