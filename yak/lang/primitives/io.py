from yak.lang.primitives.task import Task
from yak.lang.primitives.vocabulary import define_vocabulary
from yak.lang.primitives.word import define_primitive


__VOCAB__ = 'io'


def get_file_contents(task: Task):
    """( str -- str )"""
    pathname = task.datastack.pop()
    with open(pathname, mode='r', encoding='utf-8') as f:
        task.datastack.push(f.read())


def set_file_contents(task: Task):
    """( str str -- )"""
    contents = task.datastack.pop()
    pathname = task.datastack.pop()
    with open(pathname, mode='w', encoding='utf-8') as f:
        f.write(contents)


IO = define_vocabulary(__VOCAB__)
IO.store(define_primitive(__VOCAB__, 'file-contents', get_file_contents))
IO.store(define_primitive(__VOCAB__, 'file-contents=', set_file_contents))
