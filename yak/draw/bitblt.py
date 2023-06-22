from dataclasses import dataclass
from enum import Enum

from .color import Color
from .geometry import Rectangle


class CombinationRule(Enum):
    pass


@dataclass
class BitBlt:
    destination:
    source:
    fill: Color
    combination_rule: CombinationRule
    destination_origin:
    source_origin:
    extent: Rectangle
    clipping_rect: Rectangle

    def draw_from_to(self):
        pass

    def draw_loop(self):
        pass

    def copy_bits(self):
        pass
