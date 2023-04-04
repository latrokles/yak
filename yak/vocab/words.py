from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_compound, def_primitive


def define_word(interpreter):
    """( word defn -- )"""
    # TODO add stack effect
    # TODO add stack effect cheking
    # TODO add word metadata
    # TODO add word docs
    defn = interpreter.datastack.pop()
    name = interpreter.datastack.pop()
    word = def_compound(interpreter.current_vocab, name, defn)
    interpreter.store_word(word)

__VOCAB__ = 'words'
WORDS = (def_vocabulary('words')
         .store(def_primitive(__VOCAB__, 'define-word', define_word)))
