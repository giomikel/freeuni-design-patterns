import io
import sys

from app import channel, cli, user


def test_channel_interactor_subscribe_user() -> None:
    ci = cli.ChannelInteractor()
    ch = channel.Channel("channel")
    usr = user.User("user")
    assert len(ch.get_observers()) == 0
    ci.subscribe_user(ch, usr)
    assert len(ch.get_observers()) == 1


def test_channel_interactor_unsubscribe_user() -> None:
    ci = cli.ChannelInteractor()
    ch = channel.Channel("channel")
    usr = user.User("user")
    ch.attach(usr)
    assert len(ch.get_observers()) == 1
    ci.unsubscribe_user(ch, usr)
    assert len(ch.get_observers()) == 0


def test_channel_interactor_publish_video() -> None:
    ci = cli.ChannelInteractor()
    ch = channel.Channel("channel")
    usr = user.User("user")
    ci.subscribe_user(ch, usr)
    output = io.StringIO()
    sys.stdout = output
    ci.publish_video(ch)
    sys.stdout = sys.__stdout__
    assert output.getvalue() == "Notifying subscribers of channel\n user\n"


def test_subscribe_command() -> None:
    ci = cli.ChannelInteractor()
    ch = channel.Channel("channel")
    usr = user.User("user")
    sc = cli.SubscribeCommand(ci, ch, usr)
    assert len(ch.get_observers()) == 0
    sc.execute()
    assert len(ch.get_observers()) == 1


def test_publish_command() -> None:
    ci = cli.ChannelInteractor()
    ch = channel.Channel("channel")
    usr = user.User("user")
    ch.attach(usr)
    sc = cli.PublishCommand(ci, ch)
    output = io.StringIO()
    sys.stdout = output
    sc.execute()
    sys.stdout = sys.__stdout__
    assert output.getvalue() == "Notifying subscribers of channel\n user\n"


def test_invoker_process_line1() -> None:
    usr = user.User("user")
    ch = channel.Channel("channel")
    ch.attach(usr)
    user_dict = {"user": usr}
    channel_dict = {"channel": ch}
    invoker = cli.Invoker()
    command = invoker.process_line(
        "subscribe <user> to <channel>", channel_dict, user_dict
    )
    assert isinstance(command, cli.Command)


def test_invoker_process_line2() -> None:
    usr = user.User("user")
    ch = channel.Channel("channel")
    ch.attach(usr)
    user_dict = {"user": usr}
    channel_dict = {"channel": ch}
    invoker = cli.Invoker()
    command = invoker.process_line(
        "publish video on <channel>", channel_dict, user_dict
    )
    assert isinstance(command, cli.Command)


def test_invoker_process_line3() -> None:
    usr = user.User("user")
    ch = channel.Channel("channel")
    ch.attach(usr)
    user_dict = {"user": usr}
    channel_dict = {"channel": ch}
    invoker = cli.Invoker()
    command = invoker.process_line(
        "publish something something", channel_dict, user_dict
    )
    assert command is None


def test_invoker_run() -> None:
    usr = user.User("user")
    ch = channel.Channel("channel")
    user_dict = {"user": usr}
    channel_dict = {"channel": ch}
    invoker = cli.Invoker()
    command = invoker.process_line(
        "subscribe <user> to <channel>", channel_dict, user_dict
    )
    assert len(ch.get_observers()) == 0
    invoker.run(command)
    assert len(ch.get_observers()) == 1
