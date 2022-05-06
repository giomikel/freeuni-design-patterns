from typing import Dict

from app.channel import Observable
from app.cli import Invoker
from app.data_manager import SQLiteIOManager, SQLiteProcessor
from app.user import Observer


class Driver:
    def __init__(self) -> None:
        self.invoker: Invoker = Invoker()
        self.channels: Dict[str, Observable] = dict()
        self.users: Dict[str, Observer] = dict()

    def read_sqlite(self, file_name: str, table_name: str) -> None:
        io_manager = SQLiteIOManager(table_name)
        data_processor = SQLiteProcessor()
        data = io_manager.read(file_name)
        data = data_processor.extract(data)
        self.channels, self.users = data_processor.format_for_driver(data)

    def write_sqlite(self, file_name: str, table_name: str) -> None:
        io_manager = SQLiteIOManager(table_name)
        data_processor = SQLiteProcessor()
        data = data_processor.format_for_insertion((self.channels, self.users))
        io_manager.write_all(file_name, data)

    def run(self) -> None:
        print("Commands:")
        print("subscribe <username> to <channel>")
        print("publish video on <channel>")
        print("exit")
        while True:
            line = input()
            if line == "exit":
                break
            command = self.invoker.process_line(line, self.channels, self.users)
            if command:
                self.invoker.run(command)


if __name__ == "__main__":
    driver = Driver()
    driver.read_sqlite("test.db", "test1")
    driver.run()
    driver.write_sqlite("test.db", "test2")
