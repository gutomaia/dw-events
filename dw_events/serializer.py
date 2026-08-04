import importlib
import json

from dw_core.cqrs import Event


def serialize_class(class_):
    if hasattr(class_, '__qualname__'):
        classname = class_.__qualname__
    else:
        classname = class_.__class__.__name__

    if classname == 'function':
        classname = class_.__name__

    return dict(
        __module__=class_.__module__,
        __class__=classname,
    )


def unserialize_class(data):
    # READ, never pop: callers inspect a serialized handler and
    # then forward the same dict onward — mutating it here handed
    # celery workers an empty payload (measured).
    module_name = data['__module__']
    class_name = data['__class__']
    module = importlib.import_module(module_name)
    model_class = getattr(module, class_name)
    return model_class


def serialize_handle(handle):
    pass


def serialize_event(event: Event):
    return json.dumps(
        {
            **serialize_class(event),
            **event.model_dump(),
        }
    )


def unserialize_event(serialized_data: str):
    data = json.loads(serialized_data)
    model_class = unserialize_class(data)
    data.pop('__module__', None)
    data.pop('__class__', None)
    obj = model_class(**data)
    return obj
