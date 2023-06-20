from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_primitive


def global_namespace(interpreter):
    """( -- global )"""
    interpreter.datastack.push(interpreter.GLOBAL)


def get_global(interpreter):
    """( variable -- value )"""
    var = interpreter.datastack.pop()
    value = interpreter.GLOBAL.get_binding(var)
    interpreter.datastack.push(value)


def set_global(interpreter):
    """( value variable -- )"""
    interpreter.datastack.check_available(2)
    value = interpreter.datastack.pop()
    var = interpreter.datastack.pop()
    interpreter.GLOBAL.set_binding(var, value)

def namespace(interpreter):
    """( -- namespace )"""
    interpreter.datastack.push(interpreter.namestack.peek())


def getvar(interpreter):
    """( variable -- value )"""
    interpreter.datastack.push(interpreter.get_variable())


def setvar(interpreter):
    """( value variable -- )"""
    interpreter.datastack.check_available(2)
    var = interpreter.datastack.pop()
    value = interpreter.datastack.pop()
    interpreter.set_variable(value, var)
