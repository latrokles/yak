import importlib

from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_primitive
from yak.vocab.quotations import make_quotation


def import_object(interpreter):
    """( str str -- obj )"""
    interpreter.datastack.check_available(2)
    name = interpreter.datastack.pop()
    path = interpreter.datastack.pop()

    module = load_module(path)
    objekt = getattr(module, name)

    interpreter.datastack.push(objekt)


def get_attribute(interpreter):
    """( obj str -- obj )"""
    interpreter.datastack.check_available(2)
    name = interpreter.datastack.pop()
    objekt = interpreter.datastack.pop()
    value = getattr(objekt, name)
    interpreter.datastack.push(value)


def make_args(interpreter):
    """( ... x -- quot )"""
    make_quotation(interpreter)


def make_kwargs(interpreter):
    """( ... x -- assoc )"""
    # TODO implement (needs assoc parsing)
    pass


def invoke(interpreter):
    """( fn quot -- obj )"""
    interpreter.datastack.check_available(2)
    args = interpreter.datastack.pop()
    func = interpreter.datastack.pop()
    interpreter.datastack.push(func(*args))


def invoke_and_discard_result(interpreter):
    """( fn quot -- )"""
    invoke(interpreter)
    interpreter.datastack.pop()


__VOCAB__ = 'ffi'
FFI = (def_vocabulary(__VOCAB__)
       .store(def_primitive(__VOCAB__, 'import', import_object))
       .store(def_primitive(__VOCAB__, 'attr>', get_attribute))
       .store(def_primitive(__VOCAB__, 'make-args', make_args))
       .store(def_primitive(__VOCAB__, 'make-kwargs', make_kwargs))
       .store(def_primitive(__VOCAB__, 'invoke', invoke))
       .store(def_primitive(__VOCAB__, 'invoke-no-result', invoke)))