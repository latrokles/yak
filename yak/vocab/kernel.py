from yak.interpreter import Interpreter
from yak.primitives import Value, YakPrimitive
from yak.primitives import print_object
from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_primitive

__VOCAB__ = 'kernel'


def swap(interpreter: Interpreter) -> None:
    """( a b -- b a )"""
    stack = interpreter.datastack
    stack[-1], stack[-2] = stack[-2], stack[-1]


def print_line(interpreter: Interpreter) -> None:
    """( any -- )"""
    value = interpreter.datastack.pop()
    print(print_object(value))


def show_stack(interpreter: Interpreter) -> None:
    """( -- )"""
    interpreter.datastack.push(interpreter.datastack)
    print('---- data stack:')
    print_line(interpreter)


KERNEL = (def_vocabulary(__VOCAB__)
          .store(def_primitive(__VOCAB__, 'print-line', print_line))
          .store(def_primitive(__VOCAB__, 'show-stack', show_stack))
          .store(def_primitive(__VOCAB__, 'swap', swap)))
