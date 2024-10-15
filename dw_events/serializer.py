from dw_core.cqrs import Event
import json
import importlib


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
    module_name = data.pop('__module__')
    class_name = data.pop('__class__')
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
    obj = model_class(**data)
    return obj
