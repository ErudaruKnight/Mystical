from typing import Optional, Dict, List
from .sigil import Sigil

class RuneCircle:
    def __init__(self):
        self.core: Optional[Sigil] = None
        self.layers: Dict[int, List[Optional[Sigil]]] = {
            i: [None for _ in range(5)] for i in range(1, 6)
        }

    def add_sigil(self, sigil: Sigil):
        if sigil.level == 0:
            self.core = sigil
        elif 1 <= sigil.level <= 5 and 0 <= sigil.position <= 4:
            self.layers[sigil.level][sigil.position] = sigil
        else:
            raise ValueError("Неверный уровень или позиция сигила")
