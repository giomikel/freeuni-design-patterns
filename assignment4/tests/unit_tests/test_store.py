import pytest

from app.core.item import item
from app.core.receipt import receipt
from app.core.receipt.receipt import AbstractReceipt, Receipt
from app.core.store import store


@pytest.fixture
def x_report() -> store.XReport:
    rp = store.XReport()
    return rp


def test_x_report_add_receipt_to_report(x_report: store.XReport) -> None:
    it = item.Item("Water", 1.0)
    _receipt = Receipt()
    _receipt.add(it)
    assert len(x_report.get_report()) == 0
    x_report.add_receipt_to_report(_receipt)
    assert len(x_report.get_report()) == 1


def test_x_report_get_report(x_report: store.XReport) -> None:
    assert isinstance(x_report.get_report(), dict) is True
    it = item.Item("Water", 1.0)
    _receipt = Receipt()
    _receipt.add(it)
    x_report.add_receipt_to_report(_receipt)
    assert len(x_report.get_report()) == 1


def test_x_report_get_revenue(x_report: store.XReport) -> None:
    assert x_report.get_revenue() == 0
    it = item.Item("Water", 1.0)
    _receipt = Receipt()
    _receipt.add(it)
    x_report.add_receipt_to_report(_receipt)
    assert x_report.get_revenue() == 1.0


def test_x_report_get_closed_receipt_count(x_report: store.XReport) -> None:
    assert x_report.get_closed_receipt_count() == 0
    it = item.Item("Water", 1.0)
    _receipt = Receipt()
    _receipt.add(it)
    x_report.add_receipt_to_report(_receipt)
    assert x_report.get_closed_receipt_count() == 1


@pytest.fixture
def csr() -> store.AbstractCashier:
    csr = store.Cashier()
    it = item.Item("Water", 1.0)
    csr.add(it)
    return csr


def test_cashier_open_receipt(csr: store.AbstractCashier) -> None:
    csr.close_paid_receipt(True)
    csr.open_receipt()
    it = item.Item("Milk", 2.2)
    assert isinstance(csr.add(it), receipt.Receipt) is True
    assert len(csr.add(it).get_items()) == 2


def test_cashier_add(csr: store.AbstractCashier) -> None:
    it = item.Item("Milk", 2.2)
    rcpt = csr.add(it)
    assert isinstance(rcpt, AbstractReceipt) is True
    assert len(rcpt.get_items()) == 2


def test_cashier_close_paid_receipt(csr: store.AbstractCashier) -> None:
    csr.close_paid_receipt(True)
    it = item.Item("Milk", 2.2)
    csr.add(it)
    assert len(csr.get_receipt().get_items()) == 1


def test_cashier_get_receipt(csr: store.AbstractCashier) -> None:
    assert isinstance(csr.get_receipt(), AbstractReceipt) is True
    assert len(csr.get_receipt().get_items()) == 1
