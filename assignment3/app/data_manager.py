import sqlite3
from typing import Any, Dict, Protocol, Set, Tuple

from app.channel import Channel, Observable
from app.user import Observer, User


class IOManager(Protocol):
    def read(self, file_name: str) -> str:
        ...

    def write(self, file_name: str, channel: str, user: str) -> None:
        ...


class SQLiteIOManager:
    def __init__(self, table_name: str) -> None:
        self.table_name = table_name

    def read(self, file_name: str) -> str:
        conn = sqlite3.connect(file_name)
        curs = conn.cursor()
        table_exists = curs.execute(
            "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{}'".format(
                self.table_name
            )
        ).fetchone()[0]
        result = (
            curs.execute("SELECT * FROM {}".format(self.table_name)).fetchall()
            if table_exists
            else []
        )
        curs.close()
        conn.close()
        return str(result)

    def write(self, file_name: str, channel: str, user: str) -> None:
        pair: Tuple[str, str] = (channel, user)
        data: Set[Tuple[str, str]] = set()
        data.add(pair)
        self.write_all(file_name, data)

    def write_all(self, file_name: str, data: Set[Tuple[str, str]]) -> None:
        conn = sqlite3.connect(file_name)
        curs = conn.cursor()
        curs.execute(
            """CREATE TABLE IF NOT EXISTS {}
                        (
                            channel TEXT NOT NULL,
                            username TEXT NOT NULL,
                            UNIQUE(channel, username)
                        )""".format(
                self.table_name
            )
        )
        for channel, user in data:
            curs.execute(
                "INSERT OR IGNORE INTO {} VALUES (?, ?)".format(self.table_name),
                (channel, user),
            )
        conn.commit()
        curs.close()
        conn.close()


class InMemoryIOManager:
    def __init__(self) -> None:
        self.files: Dict[str, str] = {}

    def read(self, file_name: str) -> str:
        if file_name in self.files:
            return self.files[file_name]
        else:
            return ""

    def write(self, file_name: str, channel: str, user: str) -> None:
        if file_name in self.files:
            self.files[file_name] += channel + " " + user + " "
        else:
            self.files[file_name] = channel + " " + user + " "


class DataProcessor(Protocol):
    def extract(self, data: str) -> Any:
        ...

    def format_for_driver(
        self, data: Any
    ) -> Tuple[Dict[str, Observable], Dict[str, Observer]]:
        ...

    def format_for_insertion(
        self, data: Tuple[Dict[str, Observable], Dict[str, Observer]]
    ) -> Any:
        ...


class SQLiteProcessor:
    def extract(self, data: str) -> Dict[str, Set[str]]:
        comma_separated = (
            data.strip("][)")
            .replace("(", "")
            .replace(")", "")
            .replace("'", "")
            .split(", ")
        )
        pairs = list(zip(comma_separated[::2], comma_separated[1::2]))
        result_dict: Dict[str, Set[str]] = {}
        for pair in pairs:
            if pair[0] in result_dict:
                result_dict[pair[0]].add(pair[1])
            else:
                temp_set = set()
                temp_set.add(pair[1])
                result_dict[pair[0]] = temp_set
        return result_dict

    def format_for_driver(
        self, data: Dict[str, Set[str]]
    ) -> Tuple[Dict[str, Observable], Dict[str, Observer]]:
        channels = dict()
        users = dict()
        for channel_name, user_set in data.items():
            channel = Channel(channel_name)
            for user_name in user_set:
                user = User(user_name)
                channel.attach(user)
                users[user_name] = user
            channels[channel_name] = channel
        return channels, users

    def format_for_insertion(
        self, data: Tuple[Dict[str, Observable], Dict[str, Observer]]
    ) -> Set[Tuple[str, str]]:
        channels, users = data
        result_set = set()
        for channel_name, channel_obj in channels.items():
            for user_obj in channel_obj.get_observers():
                result_set.add((channel_name, user_obj.get_name()))
        return result_set
