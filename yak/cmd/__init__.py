from yak.util import set_up_yakdir
from yak.vm import YakVirtualMachine


def yak():
    set_up_yakdir()
    return YakVirtualMachine().init()
