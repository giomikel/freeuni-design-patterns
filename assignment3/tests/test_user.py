import io
import sys

import pytest

from app import user as user_file


@pytest.fixture()
def user() -> user_file.User:
    usr = user_file.User("name")
    return usr


def test_user_get_name(user: user_file.User) -> None:
    assert user.get_name() == "name"


def test_user_update(user: user_file.User) -> None:
    output = io.StringIO()
    sys.stdout = output
    user.update()
    sys.stdout = sys.__stdout__
    assert output.getvalue() == " name\n"
