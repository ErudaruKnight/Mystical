from typing import Optional, Dict, List
from .sigil import Sigil

class RuneCircle:
    def __init__(self):
        self.core: Optional[Sigil] = None
        # Single ring with five sockets
        self.layers: Dict[int, List[Optional[Sigil]]] = {
            1: [None for _ in range(5)]
        }

    def add_sigil(self, sigil: Sigil):
        if sigil.level == 0:
            self.core = sigil
        elif sigil.level == 1 and 0 <= sigil.position <= 4:
            self.layers[1][sigil.position] = sigil
        else:
            raise ValueError("Неверный уровень или позиция сигила")
