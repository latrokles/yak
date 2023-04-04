from yak.primitives.quotation import Quotation
from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_primitive



def make_quotation(interpreter):
    """( ... x -- quot )"""
    x = interpreter.datastack.peek()
    interpreter.datastack.check_available(x + 1)

    x = interpreter.datastack.pop()
    contents = [ interpreter.datastack.pop() for _ in range(x) ]
    contents.reverse()
    interpreter.datastack.push(Quotation(contents))



__VOCAB__ = 'quotations'
QUOTATIONS = (def_vocabulary(__VOCAB__)
              .store(def_primitive(__VOCAB__, 'make-quotation', make_quotation)))
