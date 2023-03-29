from yak.lang.primitives.task import Task
from yak.lang.primitives.vocabulary import define_vocabulary
from yak.lang.primitives.word import define_primitive


def true(task: Task):
    """( -- t )"""
    task.datastack.push(True)


def false(task: Task):
    """( -- f )"""
    task.datastack.push(False)


def nil(task: Task):
    """( -- nil )"""
    task.datastack.push(None)


SYNTAX = define_vocabulary('syntax')
SYNTAX.store(define_primitive(SYNTAX.name, 't', true))
SYNTAX.store(define_primitive(SYNTAX.name, 'f', false))
SYNTAX.store(define_primitive(SYNTAX.name, 'nil', nil))

