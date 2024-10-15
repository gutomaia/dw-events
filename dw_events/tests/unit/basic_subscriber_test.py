from unittest import TestCase

from dw_core.cqrs import Event
from dw_events.tests.event_subscriber_spec import (
    EventSubscriberSpec,
    ExecuterType,
)
from dw_events.adapters import BasicSubscriber


class BasicSubscriberTest(EventSubscriberSpec, TestCase):
    def setUp(self) -> None:
        self.es = BasicSubscriber()

    def given_subscription(
        self, event_class: type[Event], executer: ExecuterType
    ):
        self.es.subscribe(event_class, executer)

    def when_get_subscriber(self, event_class: Event):
        self.subs = self.es.get_subscribers(event_class)

    def assert_subscriber_has(self, executer: ExecuterType):
        self.assertIn(executer, self.subs)

    def assert_subscribers_length(self, size):
        self.assertEqual(len(self.subs), size)
