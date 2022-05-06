import datetime
from dataclasses import dataclass
from typing import Dict

from app.core.store.cashier_interactor import ReceiptRepository
from app.core.store.store import XReport


@dataclass
class XReportRequest:
    date: datetime.date


@dataclass
class XReportResponse:
    revenue: float
    items: Dict[str, int]
    closed_receipts_count: int


@dataclass
class ManagerInteractor:
    receipt_repository: ReceiptRepository

    def make_x_report(self, request: XReportRequest) -> XReportResponse:
        receipts = self.receipt_repository.get_receipts_from_date(request.date)
        x_rep = XReport()
        for rcpt in receipts:
            x_rep.add_receipt_to_report(rcpt)
        return XReportResponse(
            x_rep.get_revenue(), x_rep.get_report(), x_rep.get_closed_receipt_count()
        )
