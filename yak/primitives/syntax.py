from yak.interpreter import Interpreter
from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_primitive


def true(interpreter: Interpreter):
    """( -- t )"""
    interpreter.datastack.push(True)


def false(interpreter: Interpreter):
    """( -- f )"""
    interpreter.datastack.push(False)


def nil(interpreter: Interpreter):
    """( -- nil )"""
    interpreter.datastack.push(None)


SYNTAX = def_vocabulary('syntax')
SYNTAX.store(def_primitive(SYNTAX.name, 't', true))
SYNTAX.store(def_primitive(SYNTAX.name, 'f', false))
SYNTAX.store(def_primitive(SYNTAX.name, 'nil', nil))
