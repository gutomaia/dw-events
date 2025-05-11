from typing import Callable, get_type_hints
from unittest import TestCase
from unittest.mock import Mock
from dw_core.cqrs import Event
from dw_events.tests.emit_spec import EmitSpec
from dw_events.ports import EventEmitter
from dw_events.adapters import AbstractEventEmitter
from dw_events.adapters import BasicSubscriber
from dw_events.serializer import unserialize_event
from dw_events.task import is_event_function
from dw_events.core import emit
import inject


class BasicEventEmitter(AbstractEventEmitter):
    def __init__(self, subscriber: BasicSubscriber):
        super().__init__(subscriber)

    def serialized_emit(self, serialized_event: str):
        event = unserialize_event(serialized_event)
        handlers = self.subscriber.get_subscribers(event.__class__)
        for handler in handlers:
            if is_event_function(handler):
                handler(event)


class EmitTest(EmitSpec, TestCase):
    def setUp(self) -> None:
        self.bs = BasicSubscriber()
        self.event_emitter = BasicEventEmitter(self.bs)
        self.mocks = {}

    def given_subscribed_port(self, port: Callable[[Event], None]):
        hints = get_type_hints(port)
        params = [v for k, v in hints.items() if k != 'return']
        if len(params) == 1 and issubclass(params[0], Event):
            mock = Mock(spec=port)
            mock.__annotations__ = get_type_hints(port)
            mock.side_effect = port
            self.mocks[port] = mock
            self.bs.subscribe(params[0], mock)

    def when_emit(self, event: Event):
        self.event_emitter.emit(event)

    def assert_triggered(self, func: Callable[[Event], None]):
        self.assertIn(func, self.mocks)
        self.mocks[func].assert_called()


class EmitHandlerTest(EmitTest):
    def setUp(self):
        super().setUp()
        inject.configure(
            lambda binder: binder.bind(EventEmitter, self.event_emitter),
            clear=True,
        )

    def when_emit(self, event: Event):
        emit(event)
