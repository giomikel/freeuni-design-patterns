import io
import sys

import pytest

from app import channel as channel_file
from app import user as user_file


@pytest.fixture()
def channel() -> channel_file.Channel:
    chn = channel_file.Channel("channel")
    return chn


def test_channel_attach(channel: channel_file.Channel) -> None:
    usr = user_file.User("user")
    assert len(channel.get_observers()) == 0
    channel.attach(usr)
    assert len(channel.get_observers()) == 1


def test_channel_detach(channel: channel_file.Channel) -> None:
    usr = user_file.User("user")
    channel.attach(usr)
    assert len(channel.get_observers()) == 1
    channel.detach(usr)
    assert len(channel.get_observers()) == 0


def test_channel_notify(channel: channel_file.Channel) -> None:
    usr = user_file.User("user")
    channel.attach(usr)
    output = io.StringIO()
    sys.stdout = output
    channel.notify()
    sys.stdout = sys.__stdout__
    assert output.getvalue() == "Notifying subscribers of channel\n user\n"


def test_channel_get_observers(channel: channel_file.Channel) -> None:
    usr = user_file.User("user")
    channel.attach(usr)
    assert channel.get_observers().pop() == usr
    assert len(channel.get_observers()) == 0
