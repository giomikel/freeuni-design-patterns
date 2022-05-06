from app import data_manager
from app.channel import Channel
from app.user import User


def test_io_manager_read() -> None:
    io_manager = data_manager.InMemoryIOManager()
    io_manager.write("test.txt", "channel", "user")
    assert io_manager.read("test.txt") == "channel user "


def test_io_manager_write() -> None:
    io_manager = data_manager.InMemoryIOManager()
    assert io_manager.read("test.txt") == ""
    io_manager.write("test.txt", "channel", "user")
    assert io_manager.read("test.txt") == "channel user "


def test_sqlite_processor_extract() -> None:
    processor = data_manager.SQLiteProcessor()
    extracted = processor.extract("[('channel1', 'user1'), ('channel2', 'user2')]")
    assert extracted == {"channel1": {"user1"}, "channel2": {"user2"}}


def test_sqlite_processor_format_for_driver() -> None:
    processor = data_manager.SQLiteProcessor()
    test_dict = processor.extract("[('channel1', 'user1'), ('channel2', 'user2')]")
    assert processor.format_for_driver(test_dict) == (
        {
            "channel1": Channel(name="channel1", subscribers={User("user1")}),
            "channel2": Channel(name="channel2", subscribers={User("user2")}),
        },
        {"user1": User("user1"), "user2": User("user2")},
    )


def test_sqlite_processor_format_for_insertion() -> None:
    processor = data_manager.SQLiteProcessor()
    data = (
        {
            "channel1": Channel(name="channel1", subscribers={User("user1")}),
            "channel2": Channel(name="channel2", subscribers={User("user2")}),
        },
        {"user1": User("user1"), "user2": User("user2")},
    )
    assert processor.format_for_insertion(data) == {
        ("channel1", "user1"),
        ("channel2", "user2"),
    }
