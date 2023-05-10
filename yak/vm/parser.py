from dataclasses import InitVar, dataclass, field
from enum import Enum
from typing import Callable, ClassVar

from yak.vm.chunk import Chunk
from yak.vm.opcode import Opcode
from yak.vm.scanner import Scanner, Token
from yak.vm.value import Value


def is_int(val: str) -> bool:
    try:
        int(val)
        return True
    except ValueError:
        return False


def is_float(val: str) -> bool:
    try:
        float(val)
        return True
    except ValueError:
        return False

def is_string(val: str) -> bool:
    val = str(val)
    return val.startswith('"') and val.endswith('"')


class ParseError(Exception):
    """Raised whenever an error is encountered during scanning."""


@dataclass
class Parser:
    compiler: ...
    scanner: Scanner
    EOF: ClassVar[str] = '#EOF#'

    def parse(self) -> None:
        while (value := self.next_value()) != Parser.EOF: pass

    def next_value(self) -> Value:
        try:
            if (token := self.scanner.scan_token()) is None:
                return Parser.EOF
            return self.parse_value(token)
        except Exception as e:
            print(e)
            raise ParseError(f'Unable to parse value error={e}')

    def parse_value(self, token: Token) -> Value:
        if is_int(token.text):
            return self._emit_literal(int(token.text))

        if is_float(token.text):
            return self._emit_literal(float(token.text))

        if is_string(token.text):
            return self._emit_literal(token.text[1:-1])

        return self._emit_word(token)

    def _emit_literal(self, value: Value) -> Value:
        constant = self.compiler.make_constant(value)
        self.compiler.emit_bytes(Opcode.OP_CONSTANT, constant, self.scanner.row)

    def _emit_word(self, token: Token) -> Value:
        # TODO do proper word lookup
        match token.text:
            case '+':
                self.compiler.emit_byte(Opcode.OP_ADD, self.scanner.row)
                return token.text
            case '-':
                self.compiler.emit_byte(Opcode.OP_SUBTRACT, self.scanner.row)
                return token.text
            case '*':
                self.compiler.emit_byte(Opcode.OP_MULTIPLY, self.scanner.row)
                return token.text
            case '/':
                self.compiler.emit_byte(Opcode.OP_DIVIDE, self.scanner.row)
                return token.text
            case 'neg':
                self.compiler.emit_byte(Opcode.OP_NEGATE, self.scanner.row)
                return token.text
            case '=':
                self.compiler.emit_byte(Opcode.EQUAL, self.scanner.row)
                return token.text
            case '>':
                self.compiler.emit_byte(Opcode.GREATER, self.scanner.row)
                return token.text
            case '>=':
                self.compiler.emit_byte(Opcode.GREATER_THAN, self.scanner.row)
                return token.text
            case '<':
                self.compiler.emit_byte(Opcode.LESS, self.scanner.row)
                return token.text
            case '<=':
                self.compiler.emit_byte(Opcode.LESS_THAN, self.scanner.row)
                return token.text
            case 'print':
                self.compiler.emit_byte(Opcode.OP_PRINT, self.scanner.row)
                return token.text
            case 'set-global':
                self.compiler.emit_byte(Opcode.OP_DEFINE_GLOBAL, self.scanner.row)
                return token.text
            case 'get-global':
                self.compiler.emit_byte(Opcode.OP_GET_GLOBAL, self.scanner.row)
                return token.text
            case _:
                raise ParseError(f'Unknown word={token.text}')
