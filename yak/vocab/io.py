from yak.primitives.vocabulary import def_vocabulary
from yak.primitives.word import def_primitive


def get_file_contents(interpreter):
    """( str -- str )"""
    pathname = interpreter.datastack.pop()
    with open(pathname, mode='r', encoding='utf-8') as f:
        interpreter.datastack.push(f.read())


def set_file_contents(interpreter):
    """( str str -- )"""
    contents = interpreter.datastack.pop()
    pathname = interpreter.datastack.pop()
    with open(pathname, mode='w', encoding='utf-8') as f:
        f.write(contents)


def println(interpreter):
    """( str -- )"""
    print(interpreter.datastack.pop())


def readln(interpreter):
    """( -- str )"""
    interpreter.datastack.push(input())
