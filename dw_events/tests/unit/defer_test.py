from typing import Callable, get_type_hints
from unittest import TestCase
from unittest.mock import Mock

from dw_core.cqrs import Event

from dw_events.adapters import (
    AbstractDeferredEmitter,
    AbstractEventEmitter,
    BasicSubscriber,
)
from dw_events.ports import EventEmitter
from dw_events.serializer import unserialize_event
from dw_events.task import is_event_function
from dw_events.tests.defer_spec import DeferSpec


class BasicEventEmitter(AbstractEventEmitter):
    def __init__(self, subscriber: BasicSubscriber):
        super().__init__(subscriber)
        self.serialized_emit_called = False

    def serialized_emit(self, serialized_event: str):
        self.serialized_emit_called = True
        event = unserialize_event(serialized_event)
        handlers = self.subscriber.get_subscribers(event.__class__)
        for handler in handlers:
            if is_event_function(handler):
                handler(event)


class BasicDeferredEmitter(AbstractDeferredEmitter):
    def __init__(
        self, subscriber: BasicSubscriber, event_emitter: EventEmitter = None
    ):
        super().__init__(subscriber, event_emitter=event_emitter)
        self.defer_execution_called = False

    def defer_execution(self, event, subscribers):
        self.defer_execution_called = True

        for handler in subscribers:
            if is_event_function(handler):
                handler(event)


class DeferTest(DeferSpec, TestCase):
    def setUp(self) -> None:
        self.bs = BasicSubscriber()
        self.event_emitter = BasicEventEmitter(self.bs)
        self.deffer_emitter = BasicDeferredEmitter(self.bs, self.event_emitter)
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

    def when_defer(self, event: Event):
        try:
            self.deffer_emitter.defer_emit(event)
        except Exception:
            pass

    def assert_triggered(self, func: Callable[[Event], None]):
        self.assertIn(func, self.mocks)
        self.mocks[func].assert_called()

    def assert_deferred(self):
        self.assertTrue(self.deffer_emitter.defer_execution_called)

    def assert_emitted(self):
        self.assertTrue(self.event_emitter.serialized_emit_called)
