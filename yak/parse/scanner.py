from dataclasses import InitVar, dataclass, field
from io import StringIO

from yak.parse import Scanner, Token
from yak.primitives import YakError
from yak.primitives.strings import blank


class YakScanError(YakError):
    """Raised whenever an error is encountered during scanning."""


@dataclass
class YakScanner(Scanner):
    """
    The YakScanner consumes source text and splits it into space delimited tokens.
    """

    src_txt: InitVar[str]
    src: StringIO = field(init=False)
    src_len: int = field(init=False)

    row: int = 0
    col: int = 0
    pos: int = 0

    def __post_init__(self, src_txt: str):
        """Initialize source stream."""
        self.src = StringIO(src_txt)
        self.src_len = len(src_txt)


    def scan_token(self) -> Token|None:
        """
        Consume and return the next token in the stream.

        :returns: the next token in the stream.
        :rtype: Token.

        :raises YakScanError: when the token cannot be scanned correctly.
        """
        if self.pos == self.src_len:
            return None

        token_chars = []
        char = self.scan_char()

        while blank(char):
            char = self.scan_char()

        start = self.col
        if char == '"':
            return self.scan_string()

        while not blank(char):
            token_chars.append(char)
            char = self.scan_char()
        stop = self.col
        return Token(''.join(token_chars), start, stop, self.row)

    def scan_char(self) -> str:
        """
        Consume and return the next character in the stream.

        :returns: the next character in the stream.
        :rtype: str.
        """
        if self.pos == self.src_len:
            return ''

        char = self.src.read(1)
        self.pos += 1
        self.col += 1

        if self.src.getvalue()[self.pos - 1] == '\n':
            self.col = 0
            self.row += 1

        return char

    def scan_string(self) -> Token:
        """
        Consume characters until the closing `"` in the stream and return the
        enclosed string as a token.

        :returns: the token containing the scanned string.
        :rtype: Token.
        """
        token_chars = ['"']
        start = self.col
        char = self.scan_char()

        while char != '"' and self.pos < self.src_len:
            token_chars.append(char)
            char = self.scan_char()

        # consume the closing quote
        token_chars.append(char)
        stop = self.col
        text = ''.join(token_chars)

        if char != '"':
            message = f'Unterminated string. value={text}'
            raise YakScanError(f'{message}, line={self.row}, pos=[{start}:{stop}]')
        return Token(text, start, stop, self.row)
