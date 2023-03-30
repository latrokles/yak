from yak.lang.primitives.io import IO
from yak.lang.primitives.parse import PARSE
from yak.lang.primitives.syntax import SYNTAX
from yak.lang.primitives.task import Task
from yak.lang.primitives.vocabulary import define_vocabulary
from yak.lang.primitives.word import define_compound, define_primitive


__VOCAB__ = 'bootstrap'
__SCRIPT__ = 'library/bootstrap.yak'


def load_bootstrap_script(task: Task):
    """( -- str )"""
    task.datastack.push(__SCRIPT__)


BOOTSTRAP = define_vocabulary(__VOCAB__)
BOOTSTRAP.store(define_compound(__VOCAB__, 'load-boostrap-script', load_bootstrap_script))
BOOTSTRAP.store(define_compound(__VOCAB__,
                                'bootstrap',
                                [BOOTSTRAP.fetch('load-bootstrap-script').ref,
                                 IO.fetch('file-contents').ref,
                                 PARSE.fetch('<scanner>').ref,
                                 PARSE.fetch('parse').ref,
                                 SYNTAX.fetch('call').ref]))
