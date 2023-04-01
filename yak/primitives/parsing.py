from yak.parse.parser import YakParser
from yak.parse.scanner import YakScanner
from yak.primitives.task import Task
from yak.primitives.vocabulary import define_vocabulary
from yak.primitives.word import define_primitive


__VOCAB__ = 'parsing'


def make_scanner(task: Task) -> None:
    """( str -- scanner )"""
    src = task.datastack.pop()
    self.datastack.push(YakScanner(src))


def parse(task: Task) -> None:
    """( src -- quot )"""
    make_scanner(task)
    parser = YakScanner(task, task.datastack.pop())
    parser.parse()


PARSING = define_vocabulary(__VOCAB__)
PARSING.store(define_primitive(__VOCAB__, 'parse', parse))
