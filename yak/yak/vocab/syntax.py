from yak.parsing import ParseError
from yak.primitives.quotation import Quotation
from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_primitive
from yak.vocab.kernel import call, swap
from yak.vocab.words import define_compound


def true(interpreter):
    """( -- t )"""
    interpreter.datastack.push(True)


def false(interpreter):
    """( -- f )"""
    interpreter.datastack.push(False)


def nil(interpreter):
    """( -- nil )"""
    interpreter.datastack.push(None)


def IN(interpreter):
    """( -- )"""
    parser = interpreter.get_global('*parser*')
    with parser.raw() as p:
        vocab_name = p.next_value()
        interpreter.set_current_vocabulary(vocab_name)


def USE(interpreter):
    """( -- )"""
    parser = interpreter.get_global('*parser*')
    with parser.raw() as p:
        vocab_name = p.next_value()
        interpreter.use(vocab_name)


def PRIMITIVE(interpreter):
    """( -- )"""
    parser = interpreter.get_global('*parser*')
    with parser.raw() as p:
        interpreter.datastack.push(p.next_value())  # name
        interpreter.datastack.push(interpreter.fetch_word('define-primitive'))
        interpreter.datastack.push(p.next_value())  # module
        parser.push_exclusive_state(';')


def DEFER(interpreter):
    """( -- )"""
    parser = interpreter.get_global('*parser*')
    with parser.raw() as p:
        deferred_word = p.next_value()
        _defer_definition(interpreter, deferred_word)


def DEFER_FROM(interpreter):
    """( -- vocab deferrer words )"""
    parser = interpreter.get_global('*parser*')

    with parser.raw() as p:
        vocab = p.next_value()

        with parser.in_vocab(vocab) as scoped_p:
            while (word := scoped_p.next_value()) != ';':
                _defer_definition(interpreter, word)


def _defer_definition(interpreter, word: str):
    interpreter.datastack.push(word)
    interpreter.datastack.push(Quotation())
    define_compound(interpreter)


def DEFINE(interpreter):
    """( -- name definer-quot quot )"""
    parser = interpreter.get_global('*parser*')

    with parser.raw() as p:
        word_name = p.next_value()
        interpreter.datastack.push(word_name)
        interpreter.datastack.push(interpreter.fetch_word('define-compound'))
        interpreter.datastack.push(Quotation())
        parser.push_exclusive_state(';')


def ENDDEF(interpreter):
    """( word definer -- )"""
    parser = interpreter.get_global('*parser*')
    swap(interpreter)
    definer = interpreter.datastack.pop()
    definer.eval(interpreter)
    parser.pop_exclusive_state(';')


def START_COMMENT(interpreter):
    # TODO parse comments and add them to parsed objects
    parser = interpreter.get_global('*parser*')
    with parser.raw() as p:
        while ((raw_txt := parser.next_value()) != '|#'): pass


def L_BRACKET(interpreter):
    """( -- quot )"""
    interpreter.get_global('*parser*').push_state(']')
    interpreter.datastack.push(Quotation())


def R_BRACKET(interpreter):
    """( quot -- quot )"""
    quote = interpreter.datastack.pop()
    parser = interpreter.get_global('*parser*')
    parser.current_accumulator.append(quote)
    parser.pop_state(']')


def L_BRACE(interpreter):
    """( -- definer quot )"""
    interpreter.get_global('*parser*').push_state('}')
    interpreter.datastack.push(interpreter.fetch_word('quot>tuple'))
    interpreter.datastack.push(Quotation())


def R_BRACE(interpreter):
    """( definer quot -- obj )"""
    swap(interpreter)
    definer = interpreter.datastack.pop()
    definer.eval(interpreter)
    parser = interpreter.get_global('*parser*')
    value = interpreter.datastack.pop()
    parser.current_accumulator.append(value)
    parser.pop_state('}')


def DEFASSOC(interpreter):
    """( -- definer quot )"""
    interpreter.get_global('*parser*').push_state('}')
    interpreter.datastack.push(interpreter.fetch_word('quot>assoc'))
    interpreter.datastack.push(Quotation())


def L_PAREN(interpreter):
    # TODO implement proper stack effect parsing
    parser = interpreter.get_global('*parser*')
    with parser.raw() as p:
        while (raw_txt := parser.next_value()) != ')': pass


__VOCAB__ = 'syntax'
SYNTAX = (def_vocabulary('syntax')
          .store(def_primitive(__VOCAB__, 't', true))
          .store(def_primitive(__VOCAB__, 'f', false))
          .store(def_primitive(__VOCAB__, 'nil', nil))
          .store(def_primitive(__VOCAB__, 'IN:', IN, parse=True))
          .store(def_primitive(__VOCAB__, 'USE:', USE, parse=True))
          .store(def_primitive(__VOCAB__, 'DEFER:', DEFER, parse=True))
          .store(def_primitive(__VOCAB__, 'DEFER-FROM:', DEFER_FROM, parse=True))
          .store(def_primitive(__VOCAB__, 'PRIMITIVE:', PRIMITIVE, parse=True))
          .store(def_primitive(__VOCAB__, '#|', START_COMMENT, parse=True))
          .store(def_primitive(__VOCAB__, '[', L_BRACKET, parse=True))
          .store(def_primitive(__VOCAB__, ']', R_BRACKET, parse=True))
          .store(def_primitive(__VOCAB__, 'A{', DEFASSOC, parse=True))
          .store(def_primitive(__VOCAB__, '{', L_BRACE, parse=True))
          .store(def_primitive(__VOCAB__, '}', R_BRACE, parse=True))
          .store(def_primitive(__VOCAB__, '(', L_PAREN, parse=True))
          .store(def_primitive(__VOCAB__, ':', DEFINE, parse=True))
          .store(def_primitive(__VOCAB__, ';', ENDDEF, parse=True)))
