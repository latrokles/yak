from typing import Callable

from yak.lang.primitives import CompoundWord, PrimitiveWord, Value, Word


def define_compound(vocabulary_name: str,
                    name: str, 
                    defn: list[Value], 
                    parse: bool = False) -> Word:
    # TODO add docs
    return CompoundWord(name, vocabulary_name, parse, 'nodoc', defn)


def define_primitive(vocabulary_name: str,
                     name: str, 
                     defn: Callable,
                     parse: bool = False) -> Word:
    return PrimitiveWord(name, vocabulary_name, parse, defn.__doc__, defn)
