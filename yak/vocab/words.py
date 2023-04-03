from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_primitive, define_word

__VOCAB__ = 'words'
WORDS = (def_vocabulary('words')
         .store(def_primitive(__VOCAB__, 'define-word', define_word)))
