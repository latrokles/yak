from yak.hal import YakOS
from yak.util import set_up_yakdir


def yak():
    set_up_yakdir()
    return YakOS().init()
