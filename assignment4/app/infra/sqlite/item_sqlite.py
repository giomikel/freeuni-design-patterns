import sqlite3
from typing import Any, List, Optional

from app.core.item.item import AbstractReceiptItem, CompositeItem, Item
from app.infra.sqlite.db_util import FILE_NAME, ITEMS_TABLE_NAME


class ItemSqlite:
    def create_item(self, item: AbstractReceiptItem) -> None:
        conn = sqlite3.connect(FILE_NAME)
        curs = conn.cursor()
        curs.execute(
            """CREATE TABLE IF NOT EXISTS {}
                        (
                            item_name TEXT NOT NULL,
                            amount INTEGER NOT NULL,
                            unit_price REAL NOT NULL,
                            price REAL NOT NULL,
                            UNIQUE(item_name)
                        )""".format(
                ITEMS_TABLE_NAME
            )
        )
        curs.execute(
            """INSERT OR IGNORE INTO {} VALUES (?, ?, ?, ?)""".format(ITEMS_TABLE_NAME),
            (item.get_name(), item.get_amount(), item.get_unit_price(), item.price),
        )
        conn.commit()
        curs.close()
        conn.close()

    def get_item(self, item_name: str) -> Optional[AbstractReceiptItem]:
        conn = sqlite3.connect(FILE_NAME)
        curs = conn.cursor()
        table_exists = curs.execute(
            "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{}'".format(
                ITEMS_TABLE_NAME
            )
        ).fetchone()[0]
        result = (
            curs.execute(
                "SELECT * FROM {} WHERE item_name = ?".format(ITEMS_TABLE_NAME),
                (item_name,),
            ).fetchall()
            if table_exists
            else []
        )
        curs.close()
        conn.close()
        return self._process_result(result)

    def _process_result(self, result: List[Any]) -> Optional[AbstractReceiptItem]:
        if result:
            result_item_name = result[0][0]
            result_amount = result[0][1]
            result_unit_price = result[0][2]
            single_item = Item(result_item_name, result_unit_price)
            if result_amount == 1:
                return single_item
            else:
                composite_item = CompositeItem(result_item_name)
                for i in range(result_amount):
                    composite_item.add(single_item)
                return composite_item
        else:
            return None
