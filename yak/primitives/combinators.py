from yak.interpreter import Interpreter
from yak.primitives.vocabulary import define_vocabulary
from yak.primitives.word import define_primitive

__VOCAB__ = 'combinators'


def call(interpreter: Interpreter) -> None:
    """( quot -- | | -- quot )"""
    interpreter.call()


COMBINATORS = define_vocabulary(__VOCAB__)
COMBINATORS.store(define_primitive(__VOCAB__, 'call', call))
