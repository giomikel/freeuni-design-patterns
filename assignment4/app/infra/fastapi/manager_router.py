import datetime

from fastapi import APIRouter, Depends

from app.core.facade import ManagerService
from app.core.store.manager_interactor import XReportRequest, XReportResponse
from app.infra.fastapi.dependables import get_core_manager

manager_api = APIRouter()


@manager_api.get("/manager/x_report/{date_str}")
def make_x_report(
    date_str: str, core: ManagerService = Depends(get_core_manager)
) -> XReportResponse:
    year, month, day = date_str.split("-")
    date = datetime.date(int(year), int(month), int(day))
    return core.make_x_report(XReportRequest(date))
