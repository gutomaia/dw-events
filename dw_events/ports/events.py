from abc import ABC, abstractmethod
from typing import Type
from dw_core.cqrs import Event


__all__ = ['EventEmitter', 'EventSubscriber', 'EventHandler']


class EventEmitter(ABC):
    @abstractmethod
    def emit(self, event: Event):
        pass


class EventSubscriber(ABC):
    @abstractmethod
    def subscribe(self, event_class: Type[Event], task):
        pass

    @abstractmethod
    def get_subscribers(self, event_class: Type[Event]):
        pass

    @abstractmethod
    def autosubscribe(self):
        pass


class EventHandler(ABC):
    @abstractmethod
    def handle(event: Event):
        pass

    @abstractmethod
    def run(handler, event: Event):
        pass
