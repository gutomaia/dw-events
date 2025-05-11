from dw_core.cqrs import Event


class DeferSpec:
    def given_subscribed_port(self, notify):
        raise NotImplementedError()

    def when_defer(self, event: Event):
        raise NotImplementedError()

    def assert_triggered(self, func):
        raise NotImplementedError()

    def assert_deferred(self):
        raise NotImplementedError()

    def assert_emitted(self):
        raise NotImplementedError()

    def test_defer(self):
        class Notification(Event):
            msg: str

        def notify(notification: Notification) -> None:
            pass

        self.given_subscribed_port(notify)

        self.when_defer(Notification(msg='Hello'))

        self.assert_triggered(notify)

    def test_triggers_multiple_handlers(self):
        class NewUser(Event):
            username: str

        def send_welcome_email(new_user: NewUser):
            pass

        def send_welcome_sms(new_user: NewUser):
            pass

        self.given_subscribed_port(send_welcome_email)
        self.given_subscribed_port(send_welcome_sms)

        self.when_defer(NewUser(username='Batman'))

        self.assert_triggered(send_welcome_email)
        self.assert_triggered(send_welcome_sms)

    def test_trigger_emits_if_deffer_fails(self):
        class Fail(Event):
            code: int

        def failed(fail: Fail):
            raise Exception()

        self.given_subscribed_port(failed)

        self.when_defer(Fail(code=101))

        self.assert_deferred()
        self.assert_emitted()
