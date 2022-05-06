from dataclasses import dataclass
from typing import Protocol


class Observer(Protocol):
    def update(self) -> None:
        ...

    def get_name(self) -> str:
        ...


@dataclass
class User:
    def __init__(self, username: str) -> None:
        self.username = username

    def __hash__(self) -> int:
        return hash(self.username)

    def update(self) -> None:
        print(" " + self.username)

    def get_name(self) -> str:
        return self.username
