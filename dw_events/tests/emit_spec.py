from dw_core.cqrs import Event


class Notification(Event):
    msg: str


class NewUser(Event):
    username: str


class EmitSpec:
    def given_subscribed_port(self, notify):
        raise NotImplementedError()

    def when_emit(self, event: Event):
        raise NotImplementedError()

    def assert_triggered(self, func):
        raise NotImplementedError()

    def test_emit(self):
        def notify(notification: Notification) -> None:
            pass

        self.given_subscribed_port(notify)

        self.when_emit(Notification(msg='Hello'))

        self.assert_triggered(notify)

    def test_triggers_multiple_handlers(self):
        def send_welcome_email(new_user: NewUser):
            pass

        def send_welcome_sms(new_user: NewUser):
            pass

        self.given_subscribed_port(send_welcome_email)
        self.given_subscribed_port(send_welcome_sms)

        self.when_emit(NewUser(username='Batman'))

        self.assert_triggered(send_welcome_email)
        self.assert_triggered(send_welcome_sms)
