import pkg_resources

from yak.interpreter import Interpreter
from yak.primitives.combinators import COMBINATORS
from yak.primitives.io import IO
from yak.primitives.parsing import PARSING
from yak.primitives.quotation import Quotation
from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_compound, def_primitive


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


BOOTSTRAP = def_vocabulary(__VOCAB__)
BOOTSTRAP.store(def_primitive(__VOCAB__, 'bootstrap-script', bootstrap_script))
BOOTSTRAP.store(def_primitive(__VOCAB__, 'resource-path', resource_path))
BOOTSTRAP.store(def_compound(__VOCAB__,
                             'bootstrap',
                             Quotation([BOOTSTRAP.fetch('bootstrap-script').ref,
                                        BOOTSTRAP.fetch('resource-path').ref,
                                        IO.fetch('file-contents').ref,
                                        PARSING.fetch('parse').ref,
                                        COMBINATORS.fetch('call').ref])))
