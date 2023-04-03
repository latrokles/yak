from yak.interpreter import Interpreter
from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_primitive


__VOCAB__ = 'syntax'


def true(interpreter: Interpreter):
    """( -- t )"""
    interpreter.datastack.push(True)


def false(interpreter: Interpreter):
    """( -- f )"""
    interpreter.datastack.push(False)


def nil(interpreter: Interpreter):
    """( -- nil )"""
    interpreter.datastack.push(None)


def IN(interpreter: Interpreter):
    """( -- )"""
    parser = interpreter.get_global('*parser*')
    with parser.raw() as p:
        vocab_name = parser.next_value()
        interpreter.set_current_vocabulary(vocab_name)


SYNTAX = def_vocabulary('syntax')
SYNTAX.store(def_primitive(__VOCAB__, 't', true))
SYNTAX.store(def_primitive(__VOCAB__, 'f', false))
SYNTAX.store(def_primitive(__VOCAB__, 'nil', nil))
SYNTAX.store(def_primitive(__VOCAB__, 'IN:', IN, parse=True))
