from dataclasses import dataclass, field
from typing import Protocol, Set

from app.user import Observer


class Observable(Protocol):
    def attach(self, observer: Observer) -> None:
        ...

    def detach(self, observer: Observer) -> None:
        ...

    def notify(self) -> None:
        ...

    def get_observers(self) -> Set[Observer]:
        ...


@dataclass
class Channel:
    name: str
    subscribers: Set[Observer] = field(default_factory=set)

    def attach(self, observer: Observer) -> None:
        self.subscribers.add(observer)

    def detach(self, observer: Observer) -> None:
        self.subscribers.remove(observer)

    def notify(self) -> None:
        print("Notifying subscribers of {}".format(self.name))
        for observer in self.subscribers:
            observer.update()

    def get_observers(self) -> Set[Observer]:
        return self.subscribers
