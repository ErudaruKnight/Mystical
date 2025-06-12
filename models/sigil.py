from dataclasses import dataclass
from .elements import Element

@dataclass
class Sigil:
    element: Element
    level: int       # 0 — центр, 1-5 — внешние уровни
    position: int    # 0–4 (по кругу)
