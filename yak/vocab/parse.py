from yak.parsing import Parser, Scanner
from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_primitive


__VOCAB__ = 'parse'


def make_scanner(interpreter) -> None:
    """( str -- scanner )"""
    src = interpreter.datastack.pop()
    interpreter.datastack.push(Scanner(src))


def parse(interpreter) -> None:
    """( src -- quot )"""
    make_scanner(interpreter)
    parser = Parser(interpreter, interpreter.datastack.pop())
    parser.parse()


PARSE = (def_vocabulary(__VOCAB__)
         .store(def_primitive(__VOCAB__, 'parse', parse)))
