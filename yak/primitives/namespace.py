from dataclasses import dataclass, field

from yak.primitives import Value, YakPrimitive, YakUndefinedError


@dataclass
class Namespace(YakPrimitive):
    name: str
    bindings: dict[str, Value] = field(default_factory=dict)

    def has_binding(self, binding: str) -> bool:
        return binding in self.bindings.keys()

    def get_binding(self, binding: str) -> Value:
        if binding not in self.bindings.keys():
            raise YakUndefinedError(f'namespace `{self.name}` has no binding: {binding}')
        return self.bindings[binding]

    def set_binding(self, binding: str, value: Value):
        self.bindings[binding] = value

    def fmt(self) -> str:
        return f'*NS:{self.name}*'

    def prettyformat(self) -> str:
        contents = ' '.join(self.bindings.keys())
        return f'NS:{self.name} - bindings: {contents}'
