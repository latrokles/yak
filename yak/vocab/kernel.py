from yak.primitives import Value, YakPrimitive
from yak.primitives import print_object
from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_primitive

__VOCAB__ = 'kernel'


def call(interpreter) -> None:
    """( quot --  )"""
    interpreter.call()


def retain(interpreter):
    """( obj -- | -- obj )"""
    interpreter.retainstack.push(interpreter.datastack.pop())


def restore(interpreter):
    """( -- obj | obj -- )"""
    interpreter.datastack.push(interpreter.retainstack.pop())


def drop(interpreter):
    """( x -- )"""
    interpreter.datastack.pop()


def dup(interpreter):
    """( x -- x x )"""
    interpreter.datastack.push(interpreter.datastack.peek())


def dupd(interpreter):
    """( x y -- x x y )"""
    interpreter.datastack.check_available(2)
    interpreter.datastack.push(interpreter.datastack[-2])
    swap(interpreter)


def equal(interpreter):
    """( obj1 obj2 -- ? )"""
    interpreter.datastack.check_available(2)
    first = interpreter.datastack.pop()
    second = interpreter.datastack.pop()
    interpreter.datastack.push(first is second)


def nip(interpreter):
    """( x y -- y )"""
    interpreter.datastack.check_available(2)
    swap(interpreter)
    drop(interpreter)


def over(interpreter):
    """( x y -- x y x )"""
    interpreter.datastack.check_available(2)
    interpreter.datastack.push(interpreter.datastack[-2])


def swap(interpreter) -> None:
    """( x y -- y x )"""
    interpreter.datastack.check_available(2)
    stack = interpreter.datastack
    stack[-1], stack[-2] = stack[-2], stack[-1]


def print_line(interpreter) -> None:
    """( any -- )"""
    value = interpreter.datastack.pop()
    print(print_object(value))


def show_stack(interpreter) -> None:
    """( -- )"""
    interpreter.datastack.push(interpreter.datastack)
    print('---- data stack:')
    print_line(interpreter)


KERNEL = (def_vocabulary(__VOCAB__)
          .store(def_primitive(__VOCAB__, 'call', call))
          .store(def_primitive(__VOCAB__, '>r', retain))
          .store(def_primitive(__VOCAB__, 'r>', restore))
          .store(def_primitive(__VOCAB__, 'print-line', print_line))
          .store(def_primitive(__VOCAB__, 'show-stack', show_stack))
          .store(def_primitive(__VOCAB__, 'swap', swap)))
