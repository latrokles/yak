from yak.interpreter import Interpreter
from yak.primitives.combinators import call
from yak.primitives.kernel import swap
from yak.primitives.quotation import Quotation
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
        vocab_name = p.next_value()
        interpreter.set_current_vocabulary(vocab_name)


def DEFINE(interpreter: Interpreter):
    """( -- name definer-quot quot )"""
    parser = interpreter.get_global('*parser*')

    with parser.raw() as p:
        word_name = p.next_value()
        definer = interpreter.fetch_word('define-word')
        interpreter.datastack.push(word_name)
        interpreter.datastack.push(definer)
        interpreter.datastack.push(Quotation())
        parser.push_exclusive_state(';')


def ENDDEF(interpreter: Interpreter):
    """( word definer -- )"""
    parser = interpreter.get_global('*parser*')
    swap(interpreter)
    definer = interpreter.datastack.pop()
    definer.eval(interpreter)
    parser.pop_exclusive_state(';')


SYNTAX = def_vocabulary('syntax')
SYNTAX.store(def_primitive(__VOCAB__, 't', true))
SYNTAX.store(def_primitive(__VOCAB__, 'f', false))
SYNTAX.store(def_primitive(__VOCAB__, 'nil', nil))
SYNTAX.store(def_primitive(__VOCAB__, 'IN:', IN, parse=True))
SYNTAX.store(def_primitive(__VOCAB__, ':', DEFINE, parse=True))
SYNTAX.store(def_primitive(__VOCAB__, ';', ENDDEF, parse=True))
