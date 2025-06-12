from models.rune_circle import RuneCircle
from models.elements import Element, get_interaction_bonus

def combo_efficiency(combo: str) -> float:
    """Calculate efficiency for a 5-slot combo string."""
    parts = combo.split("-")
    elems = []
    for p in parts:
        try:
            elems.append(Element(p))
        except ValueError:
            elems.append(None)

    eff = 1.0
    for i in range(len(elems)):
        e1 = elems[i]
        if not e1:
            continue
        for j in range(i + 1, len(elems)):
            e2 = elems[j]
            if not e2:
                continue
            dist = j - i
            bonus = get_interaction_bonus(e1, e2)
            if dist == 1:
                eff += bonus
            elif dist == 2:
                eff += bonus * 0.5
    return round(eff, 2)

def sigil_distance(pos1: int, pos2: int) -> int:
    return min(abs(pos1 - pos2), 5 - abs(pos1 - pos2))

def calculate_efficiency(circle: RuneCircle) -> float:
    efficiency = 1.0

    for level, sigils in circle.layers.items():
        for i in range(5):
            s1 = sigils[i]
            if not s1:
                continue

            for j in range(i + 1, 5):
                s2 = sigils[j]
                if not s2:
                    continue

                dist = sigil_distance(i, j)
                bonus = get_interaction_bonus(s1.element, s2.element)

                if dist == 1:
                    efficiency += bonus
                elif dist == 2:
                    efficiency += bonus * 0.5

    return round(efficiency, 2)
