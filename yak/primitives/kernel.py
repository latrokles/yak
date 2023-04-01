from yak.interpreter import Interpreter
from yak.primitives import Value, YakPrimitive
from yak.primitives import print_object
from yak.primitives.vocabulary import define_vocabulary
from yak.primitives.word import define_primitive

__VOCAB__ = 'kernel'


def print_line(interpreter: Interpreter) -> None:
    """( any -- )"""
    value = interpreter.datastack.pop()
    print(print_object(value))


def show_stack(interpreter: Interpreter) -> None:
    """( -- )"""
    interpreter.datastack.push(interpreter.datastack)
    print_line(interpreter)


KERNEL = define_vocabulary(__VOCAB__)
KERNEL.store(define_primitive(__VOCAB__, 'print-line', print_line))
KERNEL.store(define_primitive(__VOCAB__, 'show-stack', show_stack))
