from yak.lang.primitives.task import Task
from yak.lang.primitives.vocabulary import define_vocabulary
from yak.lang.primitives.word import define_primitive

__VOCAB__ = 'combinators'


def call(task: Task) -> None:
    """( quot -- | | -- quot )"""
    task.call()


COMBINATORS = define_vocabulary(__VOCAB__)
COMBINATORS.store(define_primitive(__VOCAB__, 'call', call))
