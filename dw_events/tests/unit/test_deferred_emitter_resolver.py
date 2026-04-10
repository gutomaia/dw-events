from dw_core.resolver import ResolutionContext, ResolverRegistry

from dw_events.ports import DeferredEmitter
from dw_events.resolver import DeferredEmitterArgumentResolver


class FakeEmitter(DeferredEmitter):
    def defer_emit(self, event):
        return None


def test_deferred_emitter_resolver_uses_factory():
    def handler(defer: DeferredEmitter):
        return defer

    registry = ResolverRegistry()
    registry.register(DeferredEmitterArgumentResolver())

    emitter = FakeEmitter()
    kwargs = registry.resolve_kwargs(
        handler,
        ResolutionContext(
            extras={'deferred_emitter_factory': lambda: emitter}
        ),
    )

    assert kwargs['defer'] is emitter
