from __future__ import annotations

from dw_events.adapters.events import AbstractEventEmitter, BasicSubscriber
from dw_events.serializer import unserialize_event
from dw_events.task import is_event_function


class InProcessEventEmitter(AbstractEventEmitter):
    def __init__(self, subscriber: BasicSubscriber):
        super().__init__(subscriber)

    def serialized_emit(self, serialized_event: str):
        event = unserialize_event(serialized_event)
        handlers = self.subscriber.get_subscribers(event.__class__)
        for handler in handlers:
            if is_event_function(handler):
                handler(event)
