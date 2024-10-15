from unittest import TestCase
from dw_core.cqrs import Event
from dw_core.ports import BackgroundTask
from dw_core.adapters import Task
from dw_events.serializer import (
    serialize_class,
    serialize_event,
    unserialize_class,
    unserialize_event,
)


class Message(Event):
    msg: str


def handle(msg: Message):
    pass


class BackgroundJob(BackgroundTask):
    def __init__(self, msg: Message):
        self.msg = msg

    def run(self):
        pass


class Job(Task):
    def __init__(self, msg: Message):
        self.msg = msg

    def run(self):
        pass


class SerializationTest(TestCase):
    def test_serialize_event(self):
        event = Message(msg='Hello World')
        serialized = serialize_event(event)

        unserialized = unserialize_event(serialized)

        self.assertEqual(event.__class__, unserialized.__class__)
        self.assertEqual(event.msg, unserialized.msg)

    def test_serialize_function(self):
        serialized = serialize_class(handle)
        self.assertEqual(
            serialized['__module__'], 'dw_events.tests.unit.serialize_test'
        )
        self.assertEqual(serialized['__class__'], 'handle')

        unserialized = unserialize_class(serialized)
        self.assertEqual(handle, unserialized)

    def test_serialize_task_handle(self):

        serialized = serialize_class(Job)
        self.assertEqual(
            serialized['__module__'], 'dw_events.tests.unit.serialize_test'
        )
        self.assertEqual(serialized['__class__'], 'Job')

        unserialized = unserialize_class(serialized)

        self.assertEqual(Job, unserialized)

    # def assert_unserialised(self, event_class: Type[Event], **kwargs):
    #     self.assertIsNotNone(self.serialized)
    #     self.event = self.aer.unserialize(self.serialized)
    #     self.assertEqual(event_class, self.event.__class__)
    #     for k, v in kwargs.items():
    #         self.assertEqual(v, getattr(self.event, k))
