from dw_core.cqrs import Event
from dw_events.ports import EventEmitter
import inject


@inject.autoparams('event_emitter')
def emit(event: Event, event_emitter: EventEmitter):
    """
    Emits a event
    """
    event_emitter.emit(event)
