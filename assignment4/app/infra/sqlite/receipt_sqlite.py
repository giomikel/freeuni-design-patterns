import datetime
import secrets
import sqlite3
from typing import Any, List

from app.core.receipt.receipt import AbstractReceipt, Receipt
from app.infra.sqlite.db_util import FILE_NAME, ITEMS_TABLE_NAME, RECEIPTS_TABLE_NAME
from app.infra.sqlite.item_sqlite import ItemSqlite


class ReceiptSqlite:
    def write_receipt(self, receipt: AbstractReceipt) -> None:
        conn = sqlite3.connect(FILE_NAME)
        curs = conn.cursor()
        curs.execute(
            """CREATE TABLE IF NOT EXISTS {}
                        (
                            receipt_id TEXT NOT NULL,
                            item_name TEXT NOT NULL,
                            date TEXT NOT NULL,
                            FOREIGN KEY(item_name) REFERENCES {}(item_name)
                        )""".format(
                RECEIPTS_TABLE_NAME, ITEMS_TABLE_NAME
            )
        )
        str_token = secrets.token_hex(nbytes=16)
        for receipt_item in receipt.get_items():
            curs.execute(
                """INSERT OR IGNORE INTO {} VALUES (?, ?, ?)""".format(
                    RECEIPTS_TABLE_NAME
                ),
                (str_token, receipt_item.get_name(), receipt.get_date()),
            )
        conn.commit()
        curs.close()
        conn.close()

    def get_receipts_from_date(self, date: datetime.date) -> List[AbstractReceipt]:
        conn = sqlite3.connect(FILE_NAME)
        curs = conn.cursor()
        table_exists = curs.execute(
            """SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{}'""".format(
                RECEIPTS_TABLE_NAME
            )
        ).fetchone()[0]
        result = (
            curs.execute(
                """SELECT receipt_id, group_concat(item_name) FROM {} WHERE date = ? GROUP BY receipt_id""".format(
                    RECEIPTS_TABLE_NAME
                ),
                (date,),
            ).fetchall()
            if table_exists
            else []
        )
        curs.close()
        conn.close()
        return self._process_result(result)

    def _process_result(self, result: List[Any]) -> List[AbstractReceipt]:
        receipts: List[AbstractReceipt] = []
        for entry in result:
            receipt = Receipt()
            item_sqlite = ItemSqlite()
            item_names = entry[1].split(",")
            for item_name in item_names:
                item_obj = item_sqlite.get_item(item_name)
                if item_obj:
                    receipt.add(item_obj)
            receipts.append(receipt)
        return receipts
