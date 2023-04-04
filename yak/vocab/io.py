from yak.interpreter import Interpreter
from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_primitive


__VOCAB__ = 'io'


def get_file_contents(interpreter: Interpreter):
    """( str -- str )"""
    pathname = interpreter.datastack.pop()
    with open(pathname, mode='r', encoding='utf-8') as f:
        interpreter.datastack.push(f.read())


def set_file_contents(interpreter: Interpreter):
    """( str str -- )"""
    contents = interpreter.datastack.pop()
    pathname = interpreter.datastack.pop()
    with open(pathname, mode='w', encoding='utf-8') as f:
        f.write(contents)


IO = (def_vocabulary(__VOCAB__)
      .store(def_primitive(__VOCAB__, 'file-contents', get_file_contents))
      .store(def_primitive(__VOCAB__, 'file-contents=', set_file_contents)))
