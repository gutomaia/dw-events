from typing import Callable
from unittest import TestCase
from unittest.mock import patch
from dw_core.cqrs import Event
from dw_events.tests.event_handler_spec import EventHandlerSpec, execute
from dw_events.adapters import AbstractEventHandler
from dw_events.adapters import BasicSubscriber
from dw_events.serializer import unserialize_class, unserialize_event
from dw_events.task import is_event_function, is_event_task


class BasicEventHandler(AbstractEventHandler):
    def __init__(self):
        super().__init__(BasicSubscriber())

    def queue_handling(self, serialized_handler, serialized_event):
        handler = unserialize_class(serialized_handler)
        event = unserialize_event(serialized_event)

        if is_event_function(handler):
            handler(event)
        elif is_event_task(handler):
            instance = handler(event)
            instance.run()


class EventHandlerTest(EventHandlerSpec, TestCase):
    def setUp(self) -> None:
        self.event_handler = BasicEventHandler()
        self.patcher = patch(
            'dw_events.tests.event_handler_spec.execute', wraps=execute
        )
        self.mock = self.patcher.start()

    def tearDown(self) -> None:
        self.patcher.stop()

    def given_subscription(
        self, event_class: Event, executer: Callable[[Event], None]
    ):
        self.event_handler.subscriber.subscribe(event_class, executer)

    def when_event_handler(self, event: Event):
        self.event_handler.handle(event)

    def assert_handler_called(self):
        self.mock.assert_called()
