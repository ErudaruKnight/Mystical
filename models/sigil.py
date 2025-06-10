from dataclasses import dataclass
from .elements import Element


@dataclass
class Sigil:
    element: Element
    level: int
    position: int
