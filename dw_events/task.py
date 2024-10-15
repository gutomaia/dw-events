from types import NoneType
from typing import Callable, Type, List, Any, get_type_hints, Tuple, Union
import inspect
from dw_core.cqrs import Event
from dw_core.core import get_ports
from dw_core.ports import BackgroundTask
from dw_events.ports import EventSubscriber
import inject


FunctionType = Callable[[Event], None]


def filter_event_function(obj: Any) -> Tuple[bool, Type[Event]]:
    if callable(obj):
        hints = get_type_hints(obj)
        if hints.get('return') is NoneType and len(hints) == 2:
            for param in hints.values():
                if issubclass(param, Event):
                    return True, param
        elif hints.get('return') is None and len(hints) == 1:
            for param in hints.values():
                if issubclass(param, Event):
                    return True, param
    return False, None


def is_event_function(obj: Any) -> bool:
    is_event, _ = filter_event_function(obj)
    return is_event


def filter_event_task(obj: Any) -> Tuple[bool, Type[Event]]:
    if isinstance(obj, type) and issubclass(obj, BackgroundTask):
        init_signature = inspect.signature(obj.__init__)
        parameters = init_signature.parameters
        if len(parameters) == 2:
            first_param = list(parameters.values())[1]
            if issubclass(first_param.annotation, Event):
                return True, first_param.annotation
    return False, None


def is_event_task(obj: Any) -> bool:
    is_event, _ = filter_event_task(obj)
    return is_event


def filter_event_handlers(
    entries: List[Tuple[str, Union[FunctionType, Type[BackgroundTask]]]]
) -> List[Tuple[Any, Type[Event]]]:
    filtered = []
    for _, entry in entries:
        is_func, event_type = filter_event_function(entry)
        if is_func:
            filtered.append((event_type, entry))
            continue
        is_class, event_type = filter_event_task(entry)
        if is_class:
            filtered.append((event_type, entry))
    return filtered


@inject.autoparams('subscriber')
def autosubcribe(subscriber: EventSubscriber):
    ports = get_ports()
    event_handlers = filter_event_handlers(ports)
    for event_class, handler in event_handlers:
        subscriber.subscribe(event_class, handler)
