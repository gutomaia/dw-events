from typing import Any

from dw_core.resolver import ResolutionContext

from dw_events.ports import DeferredEmitter


class DeferredEmitterArgumentResolver:
    def supports(self, arg_type: Any) -> bool:
        return isinstance(arg_type, type) and issubclass(
            arg_type, DeferredEmitter
        )

    def resolve(
        self,
        *,
        arg_name: str,
        arg_type: Any,
        context: ResolutionContext,
        resolved_kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        emitter = context.extras.get('deferred_emitter')
        factory = context.extras.get('deferred_emitter_factory')

        if emitter is None and callable(factory):
            emitter = factory()

        if emitter is None:
            raise RuntimeError('DeferredEmitter not configured')

        return {arg_name: emitter}
