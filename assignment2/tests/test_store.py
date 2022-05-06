import pytest

from app import item, receipt, store


@pytest.fixture
def x_report() -> store.XReport:
    rp = store.XReport()
    it = item.Item("Cheese", 4.0)
    rp.add_to_report(it)
    return rp


def test_x_report_add_remove_report(x_report: store.XReport) -> None:
    it = item.Item("Water", 1.0)
    x_report.add_to_report(it)
    assert len(x_report.get_report()) == 2
    x_report.remove_from_report(it)
    assert len(x_report.get_report()) == 1


def test_x_report_get_report(x_report: store.XReport) -> None:
    assert isinstance(x_report.get_report(), dict) is True


def test_x_report_get_revenue(x_report: store.XReport) -> None:
    assert x_report.get_revenue() == 4


def test_x_report_reset(x_report: store.XReport) -> None:
    x_report.reset()
    assert len(x_report.get_report()) == 0


def test_z_report_clear_register(x_report: store.XReport) -> None:
    store.ZReport.clear_register(x_report)
    assert len(x_report.get_report()) == 0


@pytest.fixture
def csr() -> store.AbstractCashier:
    x_report = store.XReport()
    csr = store.Cashier(x_report)
    it = item.Item("Water", 1.0)
    csr.add(it)
    return csr


def test_cashier_open_receipt(csr: store.AbstractCashier) -> None:
    csr.open_receipt()
    it = item.Item("Milk", 2.2)
    assert isinstance(csr.add(it), receipt.Receipt) is True
    assert len(csr.add(it).get_items()) == 2


def test_cashier_add_remove(csr: store.AbstractCashier) -> None:
    it = item.Item("Milk", 2.2)
    rcpt = csr.add(it)
    assert isinstance(rcpt, receipt.Receipt) is True
    assert len(rcpt.get_items()) == 2
    assert len(csr.remove(it).get_items()) == 1


def test_cashier_close_paid_receipt(csr: store.AbstractCashier) -> None:
    csr.close_paid_receipt(True)
    it = item.Item("Milk", 2.2)
    assert len(csr.add(it).get_items()) == 1


def test_cashier_make_z_report() -> None:
    x_report = store.XReport()
    csr = store.Cashier(x_report)
    it = item.Item("Milk", 2.2)
    csr.add(it)
    assert len(x_report.get_report()) == 1
    csr.make_z_report()
    assert len(x_report.get_report()) == 0
