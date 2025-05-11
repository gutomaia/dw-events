from dw_core.cqrs import Event


def immediate_handler(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def longrun_handler(func):
    def wrapper(event: Event, *args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
