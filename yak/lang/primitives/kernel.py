from yak.lang.primitives import Value, YakPrimitive


def print_object(value: Value) -> str:
    if value is None:
        return 'nil'

    match value:
        case bool():
            return repr(value)[0].lower()
        case YakPrimitive():
            return value.print_object()
        case _:
            return repr(value)
