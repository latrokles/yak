from yak.parsing import Parser, Scanner
from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_primitive
from yak.vocab.io import get_file_contents
from yak.vocab.kernel import call


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


def parse_file(interpreter):
    """( src -- quot )"""
    get_file_contents(interpreter)
    parse(interpreter)


def run_file(interpreter):
    """( src -- )"""
    parse_file(interpreter)
    call(interpreter)


PARSE = (
    def_vocabulary(__VOCAB__)
    .store(def_primitive(__VOCAB__, 'make-scanner', make_scanner))
    .store(def_primitive(__VOCAB__, 'parse', parse))
    .store(def_primitive(__VOCAB__, 'parse-file', parse_file))
    .store(def_primitive(__VOCAB__, 'run-file', run_file))
)
