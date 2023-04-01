import pkg_resources

from yak.interpreter import Interpreter
from yak.primitives.io import IO
from yak.primitives.parsing import PARSING
from yak.primitives.combinators import COMBINATORS
from yak.primitives.vocabulary import define_vocabulary
from yak.primitives.word import define_compound, define_primitive


__VOCAB__ = 'bootstrap'
__SCRIPT__ = 'library/bootstrap.yak'


def bootstrap_script(interpreter: Interpreter):
    """( -- str )"""
    interpreter.datastack.push(__SCRIPT__)


def resource_path(interpreter: Interpreter):
    """( str -- str )"""
    pathname = interpreter.datastack.pop()
    fullpath = pkg_resources.resource_filename('yak', pathname)
    interpreter.datastack.push(fullpath)


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
