import argparse
import sys

from yak.vm.debug import disassemble_chunk
from yak.vm.chunk import Chunk
from yak.vm.opcode import Opcode
from yak.vm.vm import InterpretResult, VirtualMachine


def yak():
    args = _parse_args()
    if args.script:
        _run_file(args.script)
        return 0
    _run_repl()


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog='yak',
        description='a programming language vm'
    )
    p.add_argument('-s', '--script', type=str, help='path to the yak script to run.')
    return p.parse_args()


def _run_file(pathname: str):
    vm = VirtualMachine()

    source = _read_file(pathname)
    result = vm.interpret(source)

    if result == InterpretResult.INTERPRET_COMPILE_ERROR:
        sys.exit(65)

    if result == InterpretResult.INTERPRET_RUNTIME_ERROR:
        sys.exit(70)


def _read_file(pathname: str) -> str:
    with open(pathname, 'r') as f:
        return f.read()


def _run_repl():
    vm = VirtualMachine()
    prompt = ':> '
    while True:
        line = input(prompt)
        result = vm.interpret(line)
        if result != InterpretResult.INTERPRET_OK:
            prompt = f'{result}:> '
        else:
            prompt = ':> '

