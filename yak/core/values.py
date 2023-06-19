from __future__ import annotations

"""
This module contains `yak`'s core values.
"""

class YakPrimitive:
    def raw(self) -> str:
        return repr(self)

    def fmt(self) -> str:
        return str(self)

    def prettyfmt(self) -> str:
        return self.fmt()


class YakError(Exception, YakPrimitive):
    """Top level Yak error."""


YakVal = str | float | int | bool | None | YakPrimitive


def fmt(val: YakVal) -> str:
    if val is None:
        return 'nil'

    match val:
        case bool():
            return str(val)[0].lower()  # True -> t, False -> f
        case str():
            return value
        case tuple():
            return "{ " + " ".join(fmt(val) for v in val) + " }"
        case list():
            return "[ " + " ".join(fmt(val) for v in val) + " ]"
        case dict():
            return "D{ " + " ".join(fmt(val) for v in val.item()) + " }"
        case YakPrimitive():
            return val.fmt()
        case _:
            return str(value)
