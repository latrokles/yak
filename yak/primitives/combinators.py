from yak.primitives.task import Task
from yak.primitives.vocabulary import define_vocabulary
from yak.primitives.word import define_primitive

__VOCAB__ = 'combinators'


def call(task: Task) -> None:
    """( quot -- | | -- quot )"""
    task.call()


COMBINATORS = define_vocabulary(__VOCAB__)
COMBINATORS.store(define_primitive(__VOCAB__, 'call', call))
