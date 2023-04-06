from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_compound, def_primitive
from yak.vocab import ffi


def define_compound(interpreter):
    """( word defn -- )"""
    # TODO add stack effect
    # TODO add stack effect cheking
    # TODO add word metadata
    # TODO add word docs
    defn = interpreter.datastack.pop()
    name = interpreter.datastack.pop()
    word = def_compound(interpreter.current_vocab, name, defn)
    interpreter.store_word(word)


def define_primitive(interpreter):
    """( word str str -- )"""
    callable_defn = interpreter.datastack.pop()
    name = interpreter.datastack.pop()

    defn_path = callable_defn.split('.')
    obj_name = defn_path[-1]
    obj_path = f'yak.{".".join(defn_path[:-1])}'
    
    interpreter.datastack.push(obj_path)
    interpreter.datastack.push(obj_name)
    ffi.load_object(interpreter)
    defn = interpreter.datastack.pop()

    word = def_primitive(interpreter.current_vocab, name, defn)
    interpreter.store_word(word)


__VOCAB__ = 'words'
WORDS = (def_vocabulary('words')
         .store(def_primitive(__VOCAB__, 'define-compound', define_compound))
         .store(def_primitive(__VOCAB__, 'define-primitive', define_primitive)))
