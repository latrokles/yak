from dataclasses import dataclass


@dataclass
class Scanner:
    start: str
    current: str
    line: int
