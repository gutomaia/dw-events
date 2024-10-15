from typing import Callable, Type, Union
from dw_core.ports import BackgroundTask
from dw_core.cqrs import Event


ExecuterType = Union[Type[BackgroundTask], Callable[[Event], None]]


class EventSubscriberSpec:
    def given_subscription(
        self, event_class: Type[Event], executer: ExecuterType
    ):
        raise NotImplementedError()

    def when_get_subscriber(self, event_class: Type[Event]):
        raise NotImplementedError()

    def assert_subscriber_has(self, executer: ExecuterType):
        raise NotImplementedError()

    def assert_subscribers_length(self, size):
        raise NotImplementedError()

    def test_subscription(self):
        class MyEvent(Event):
            data: str

        def func(event: MyEvent) -> None:
            pass

        self.given_subscription(MyEvent, func)

        self.when_get_subscriber(MyEvent)

        self.assert_subscriber_has(func)

    def test_unknow_subcribers_gets_empty_array(self):
        class Unknow(Event):
            lies: str

        self.when_get_subscriber(Unknow)

        self.assert_subscribers_length(0)

    def test_multiple_subscribers(self):
        class Multi(Event):
            pass

        def sub1(event: Multi):
            pass

        def sub2(event: Multi):
            pass

        self.given_subscription(Multi, sub1)
        self.given_subscription(Multi, sub2)

        self.when_get_subscriber(Multi)

        self.assert_subscribers_length(2)
