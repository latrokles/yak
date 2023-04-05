import pkg_resources

from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_primitive
from yak.vocab.parse import run_file


__VOCAB__ = 'bootstrap'
__SCRIPT__ = 'library/bootstrap.yak'


def bootstrap_script(interpreter):
    """( -- str )"""
    interpreter.datastack.push(__SCRIPT__)


def resource_path(interpreter):
    """( str -- str )"""
    pathname = interpreter.datastack.pop()
    fullpath = pkg_resources.resource_filename('yak', pathname)
    interpreter.datastack.push(fullpath)


def bootstrap(interpreter):
    bootstrap_script(interpreter)
    resource_path(interpreter)
    run_file(interpreter)


BOOTSTRAP = (
    def_vocabulary(__VOCAB__)
    .store(def_primitive(__VOCAB__, 'bootstrap', bootstrap))
)
