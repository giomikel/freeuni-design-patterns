import re
from abc import abstractmethod
from typing import Dict, List, Optional

from app.channel import Channel, Observable
from app.user import Observer, User


class ChannelInteractor:
    @staticmethod
    def subscribe_user(channel: Observable, user: Observer) -> None:
        channel.attach(user)

    @staticmethod
    def unsubscribe_user(channel: Observable, user: Observer) -> None:
        channel.detach(user)

    @staticmethod
    def publish_video(channel: Observable) -> None:
        channel.notify()


class Command:
    @abstractmethod
    def execute(self) -> None:
        pass


class SubscribeCommand(Command):
    def __init__(
        self, receiver: ChannelInteractor, channel: Observable, user: Observer
    ) -> None:
        self.receiver = receiver
        self.channel = channel
        self.user = user

    def execute(self) -> None:
        self.receiver.subscribe_user(self.channel, self.user)


class PublishCommand(Command):
    def __init__(self, receiver: ChannelInteractor, channel: Observable) -> None:
        self.receiver = receiver
        self.channel = channel

    def execute(self) -> None:
        self.receiver.publish_video(self.channel)


class Invoker:
    def process_line(
        self, line: str, channels: Dict[str, Observable], users: Dict[str, Observer]
    ) -> Optional[Command]:
        is_subscribe_cmd = bool(
            re.match("subscribe <[a-zA-Z0-9]+> to <[a-zA-Z0-9]+>", line)
        )
        is_publish_cmd = bool(re.match("publish video on <[a-zA-Z0-9]+>", line))
        if is_subscribe_cmd:
            return self._process_subscribe_cmd(line, channels, users)
        elif is_publish_cmd:
            return self._process_publish_cmd(line, channels)
        print("Invalid command, try again")
        return None

    def _process_subscribe_cmd(
        self, line: str, channels: Dict[str, Observable], users: Dict[str, Observer]
    ) -> Command:
        between_brackets: List[str] = re.findall("<.*?>", line)
        user_name: str = between_brackets[0][1:-1]
        channel_name: str = between_brackets[1][1:-1]
        if channel_name not in channels:
            channels[channel_name] = Channel(channel_name)
        if user_name not in users:
            users[user_name] = User(user_name)
        return SubscribeCommand(
            ChannelInteractor(), channels[channel_name], users[user_name]
        )

    def _process_publish_cmd(
        self, line: str, channels: Dict[str, Observable]
    ) -> Command:
        name_index1 = line.find("<") + 1
        name_index2 = line.find(">")
        channel_name: str = line[name_index1:name_index2]
        if channel_name not in channels:
            channels[channel_name] = Channel(channel_name)
        return PublishCommand(ChannelInteractor(), channels[channel_name])

    def run(self, command: Command) -> None:
        command.execute()
