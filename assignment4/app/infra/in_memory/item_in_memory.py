from dataclasses import dataclass, field
from typing import Optional, Set

from app.core.item.item import AbstractReceiptItem


@dataclass
class ItemInMemoryRepository:
    items: Set[AbstractReceiptItem] = field(default_factory=set)

    def create_item(self, item: AbstractReceiptItem) -> None:
        self.items.add(item)

    def get_item(self, item_name: str) -> Optional[AbstractReceiptItem]:
        result = None
        for item in self.items:
            if item.get_name() == item_name:
                result = item
        return result
