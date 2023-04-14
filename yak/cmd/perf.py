import sys

from yak.machine import ConsoleYakMachine


ConsoleYakMachine(4400, False).with_script(sys.argv[1]).boot()
