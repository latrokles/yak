import pkg_resources

from yak.primitives.io import IO
from yak.primitives.parsing import PARSING
from yak.primitives.combinators import COMBINATORS
from yak.primitives.task import Task
from yak.primitives.vocabulary import define_vocabulary
from yak.primitives.word import define_compound, define_primitive


__VOCAB__ = 'bootstrap'
__SCRIPT__ = 'library/bootstrap.yak'


def bootstrap_script(task: Task):
    """( -- str )"""
    task.datastack.push(__SCRIPT__)


def resource_path(task: Task):
    """( str -- str )"""
    pathname = task.datastack.pop()
    fullpath = pkg_resources.resource_filename('yak', pathname)
    task.datastack.push(fullpath)


BOOTSTRAP = define_vocabulary(__VOCAB__)
BOOTSTRAP.store(define_primitive(__VOCAB__, 'bootstrap-script', bootstrap_script))
BOOTSTRAP.store(define_primitive(__VOCAB__, 'resource-path', resource_path))
BOOTSTRAP.store(define_compound(__VOCAB__,
                                'bootstrap',
                                [BOOTSTRAP.fetch('bootstrap-script').ref,
                                 BOOTSTRAP.fetch('resource-path').ref,
                                 IO.fetch('file-contents').ref,
                                 PARSING.fetch('parse').ref,
                                 COMBINATORS.fetch('call').ref]))
