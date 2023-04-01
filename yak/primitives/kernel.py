from yak.primitives import Value, YakPrimitive
from yak.primitives import Task, print_object
from yak.primitives.vocabulary import define_vocabulary
from yak.primitives.word import define_primitive

__VOCAB__ = 'kernel'


def print_line(task: Task) -> None:
    """( any -- )"""
    value = task.datastack.pop()
    print(print_object(value))


def show_stack(task: Task) -> None:
    """( -- )"""
    task.datastack.push(task.datastack)
    print_line(task)


KERNEL = define_vocabulary(__VOCAB__)
KERNEL.store(define_primitive(__VOCAB__, 'print-line', print_line))
KERNEL.store(define_primitive(__VOCAB__, 'show-stack', show_stack))
