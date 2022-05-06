import datetime
from dataclasses import dataclass, field
from typing import List

from app.core.receipt.receipt import AbstractReceipt


@dataclass
class ReceiptInMemoryRepository:
    receipts: List[AbstractReceipt] = field(default_factory=list)

    def write_receipt(self, receipt: AbstractReceipt) -> None:
        self.receipts.append(receipt)

    def get_receipts_from_date(self, date: datetime.date) -> List[AbstractReceipt]:
        result = []
        for receipt in self.receipts:
            if receipt.get_date() == date:
                result.append(receipt)
        return result
