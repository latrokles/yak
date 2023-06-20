from yak.primitives import Value, YakPrimitive
from yak.primitives.stack import Stack
from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_primitive

__VOCAB__ = 'kernel'


def retain(interpreter):
    """( obj -- | -- obj )"""
    interpreter.retainstack.push(interpreter.datastack.pop())


def restore(interpreter):
    """( -- obj | obj -- )"""
    interpreter.datastack.push(interpreter.retainstack.pop())


def datastack(interpreter):
    """( -- stack )"""
    stack = Stack(interpreter.datastack)
    interpreter.datastack.push(stack)


def set_datastack(interpreter):
    """( quot -- )"""
    interpreter.datastack = interpreter.datastack.pop()


def set_retainstack(interpreter):
    """( quot -- )"""
    interpreter.retainstack = interpreter.datastack.pop()


def set_errorstack(interpreter):
    """( quot -- )"""
    interpreter.errorstack = interpreter.datastack.pop()


def call(interpreter):
    """( quot --  )"""
    interpreter.call()


def execute(interpreter):
    """( word -- )"""
    interpreter.execute(interpreter.datastack.pop())


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


def pick(interpreter):
    """( x y z -- x y z x )"""
    interpreter.datastack.push(interpreter.datastack[-3])


def rotl(interpreter):
    """( x y z -- y z x )"""
    stack = interpreter.datastack
    stack[-1], stack[-2], stack[-3] = stack[-3], stack[-1], stack[-2]


def rotr(interpreter):
    """( x y z -- y z x )"""
    stack = interpreter.datastack
    stack[-1], stack[-2], stack[-3] = stack[-2], stack[-3], stack[-1]


def swap(interpreter):
    """( x y -- y x )"""
    interpreter.datastack.check_available(2)
    stack = interpreter.datastack
    stack[-1], stack[-2] = stack[-2], stack[-1]


def swapd(interpreter):
    """( x y z -- y x z )"""
    stack[-2], stack[-3] = stack[-3], stack[-2]


def if_else(interpreter):
    """( ? t-quot f-quot -- ... )"""
    interpreter.datastack.check_available(3)
    if_false = interpreter.datastack.pop()
    if_true = interpreter.datastack.pop()
    condition = interpreter.datastack.pop()

    # TODO rewrite this using stack shufflers
    if condition is True:
        interpreter.datastack.push(if_true)
        call(interpreter)
        return
    interpreter.datastack.push(if_false)
    call(interpreter)
