from abc import abstractmethod
from typing import Type
from dw_core.cqrs import Event
from dw_events.ports import EventSubscriber, EventEmitter, EventHandler
from dw_events.serializer import (
    serialize_event,
    unserialize_event,
    serialize_class,
)


class AbstractEventEmitter(EventEmitter):
    def emit(self, event: Event):
        serialized = serialize_event(event)
        self.serialized_emit(serialized)

    @abstractmethod
    def serialized_emit(serialized_event: str):
        pass


class BasicSubscriber(EventSubscriber):
    def __init__(self):
        self.subscriptions = {}

    def subscribe(self, event_class: Type[Event], task):
        if event_class not in self.subscriptions:
            self.subscriptions[event_class] = [task]
        else:
            self.subscriptions[event_class].append(task)

    def get_subscribers(self, event: Type[Event]):
        return self.subscriptions.get(event, [])

    def autosubscribe(self):
        pass


class EventHandlerRunnerMixin:
    def run(self, handler, event: Event):
        pass


class AbstractEventHandler(EventHandlerRunnerMixin, EventHandler):
    def __init__(self, subscriber: EventSubscriber):
        self.subscriber = subscriber

    def handle_serialized(self, serialized_event: Event):
        event = unserialize_event(serialized_event)
        handlers = self.subscriber.get_subscribers(event.__class__)
        for handler in handlers:
            handler_serialized = serialize_class(handler)
            self.queue_handling(handler_serialized, serialized_event)

    @abstractmethod
    def queue_handling(self, serialized_handler, serialized_event):
        pass

    def handle(self, event: Event):
        handlers = self.subscriber.get_subscribers(event.__class__)
        serialized_event = serialize_event(event)
        for handle in handlers:
            serialized_handler = serialize_class(handle)
            self.queue_handling(serialized_handler, serialized_event)
