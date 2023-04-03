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

    def print_object(self) -> str:
        contents = ' '.join(self.bindings.keys())
        return f'`{self.name}` bindings: {contents}'


def namespace(interpreter):
    """( -- namespace )"""
    interpreter.datastack.push(interpreter.namestack.peek())


def get(interpreter):
    """( variable -- value )"""
    interpreter.datastack.push(interpreter.get_variable())


def set(interpreter):
    """( value variable -- )"""
    interpreter.datastack.check_available(2)
    var = interpreter.datastack.pop()
    value = interpreter.datastack.pop()
    interpreter.set_variable(value, var)


def get_global(interpreter):
    """( variable -- value )"""
    var = interpreter.datastack.pop()
    value = interpreter.GLOBAL.get_binding(var)
    interpreter.datastack.push(value)


def set_global(interpreter):
    """( value variable -- )"""
    interpreter.datastack.check_available(2)
    var = interpreter.datastack.pop()
    value = interpreter.datastack.pop()
    interpreter.GLOBAL.set_binding(var, value)
