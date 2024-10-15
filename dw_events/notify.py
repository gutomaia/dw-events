from dw_core.cqrs import Event
from dw_events.task import Task


class Notification(Event):
    msg: str


def notify_send(notification: Notification) -> None:
    pass


class Tasker(Task):
    def __init__(self, notify: Notification):
        pass
