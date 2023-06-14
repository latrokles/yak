from dataclasses import dataclass
from enum import Enum

@enum.unique
class ParseMode(Enum):
    PARSE = 'PARSE'
    STRING = 'STRING'


@dataclass
class Parser:
    yak: ...
    scanner: ...
    exclusive: bool = False
    mode: ParseMode = ParseMode.PARSE
    data: Stack = field(default_factory=Stack)
    expected: Stack = field(default_factory=Stack)
    EOF: ClassVar[str] = '#EOF#'

    def __post_init__(self):
        self.push(Quotation())
