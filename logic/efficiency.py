from typing import List
from models.elements import Element, synergy_map
from models.rune_circle import RuneCircle
from models.sigil import Sigil


def _distance_factor(pos1: int, pos2: int) -> float:
    """Return influence factor based on distance between sigils."""
    diff = abs(pos1 - pos2)
    diff = min(diff, RuneCircle.SLOTS - diff)
    if diff == 1:
        return 1.0
    if diff == 2:
        return 0.5
    return 0.0


def compute_efficiency(circle: RuneCircle) -> float:
    total_synergy = 0.0
    for level in range(RuneCircle.MAX_LEVEL + 1):
        sigils: List[Sigil] = circle.get_level_sigils(level)
        n = len(sigils)
        for i in range(n):
            for j in range(i + 1, n):
                s1, s2 = sigils[i], sigils[j]
                factor = _distance_factor(s1.position, s2.position)
                if factor == 0:
                    continue
                synergy = synergy_map.get((s1.element, s2.element), 0.0)
                total_synergy += synergy * factor
    efficiency = (1.0 + total_synergy) * 100
    return efficiency
