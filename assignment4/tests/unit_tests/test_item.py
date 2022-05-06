import pytest

from app.core.item import item as item_file


@pytest.fixture
def item() -> item_file.Item:
    itm = item_file.Item("Name", 1.00)
    return itm


def test_item_get_amount(item: item_file.Item) -> None:
    assert item.get_amount() == 1


def test_item_get_name(item: item_file.Item) -> None:
    assert item.get_name() == "Name"


def test_item_get_unit_price(item: item_file.Item) -> None:
    assert item.get_unit_price() == 1.0


def test_item_str(item: item_file.Item) -> None:
    assert item.__str__() == "Name 1 1.00 1.00"


@pytest.fixture
def composite_item() -> item_file.CompositeItem:
    it1 = item_file.Item("Water", 1.0)
    it2 = item_file.CompositeItem("Water Pack", [it1, it1, it1])
    return it2


def test_composite_item_get_amount(composite_item: item_file.CompositeItem) -> None:
    assert composite_item.get_amount() == 3


def test_composite_item_get_name(composite_item: item_file.CompositeItem) -> None:
    assert composite_item.get_name() == "Water Pack"


def test_composite_item_get_unit_price(composite_item: item_file.CompositeItem) -> None:
    assert composite_item.get_unit_price() == 1.0


def test_composite_item_str(composite_item: item_file.CompositeItem) -> None:
    assert composite_item.__str__() == "Water Pack 3 1.00 3.00"


def test_composite_item_add(composite_item: item_file.CompositeItem) -> None:
    it = item_file.Item("Milk", 2.2)
    composite_item.add(it)
    assert len(composite_item.get_items()) == 4
