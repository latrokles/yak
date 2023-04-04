from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_primitive

__VOCAB__ = 'combinators'


def call(interpreter) -> None:
    """( quot -- | | -- quot )"""
    interpreter.call()


COMBINATORS = def_vocabulary(__VOCAB__)
COMBINATORS.store(def_primitive(__VOCAB__, 'call', call))
