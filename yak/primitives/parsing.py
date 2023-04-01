from yak.interpreter import Interpreter
from yak.parsing import Parser, Scanner
from yak.primitives.vocabulary import define_vocabulary
from yak.primitives.word import define_primitive


__VOCAB__ = 'parsing'


def make_scanner(interpreter: Interpreter) -> None:
    """( str -- scanner )"""
    src = interpreter.datastack.pop()
    self.datastack.push(Scanner(src))


def parse(interpreter: Interpreter) -> None:
    """( src -- quot )"""
    make_scanner(interpreter)
    parser = Scanner(interpreter, interpreter.datastack.pop())
    parser.parse()


PARSING = define_vocabulary(__VOCAB__)
PARSING.store(define_primitive(__VOCAB__, 'parse', parse))
