from yak.interpreter import Interpreter
from yak.primitives.vocabulary import define_vocabulary
from yak.primitives.word import define_primitive


def true(interpreter: Interpreter):
    """( -- t )"""
    interpreter.datastack.push(True)


def false(interpreter: Interpreter):
    """( -- f )"""
    interpreter.datastack.push(False)


def nil(interpreter: Interpreter):
    """( -- nil )"""
    interpreter.datastack.push(None)


SYNTAX = define_vocabulary('syntax')
SYNTAX.store(define_primitive(SYNTAX.name, 't', true))
SYNTAX.store(define_primitive(SYNTAX.name, 'f', false))
SYNTAX.store(define_primitive(SYNTAX.name, 'nil', nil))
