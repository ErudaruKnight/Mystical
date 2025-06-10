from typing import Dict, List
from .sigil import Sigil


class RuneCircle:
    """Represents a rune circle with up to five levels."""

    MAX_LEVEL = 5
    SLOTS = 5

    def __init__(self) -> None:
        # Each level stores sigils by position
        self.levels: Dict[int, Dict[int, Sigil]] = {i: {} for i in range(self.MAX_LEVEL + 1)}

    def add_sigil(self, sigil: Sigil) -> None:
        level = sigil.level
        pos = sigil.position
        if level < 0 or level > self.MAX_LEVEL:
            raise ValueError("Invalid level")
        if pos < 0 or pos >= self.SLOTS:
            raise ValueError("Invalid position")
        if pos in self.levels[level]:
            raise ValueError("Position already occupied")
        self.levels[level][pos] = sigil

    def get_level_sigils(self, level: int) -> List[Sigil]:
        return list(self.levels[level].values())

    def all_sigils(self) -> List[Sigil]:
        sigils: List[Sigil] = []
        for lvl in self.levels.values():
            sigils.extend(lvl.values())
        return sigils
