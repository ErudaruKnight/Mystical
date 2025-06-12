from collections import defaultdict
from typing import Dict

from models.elements import Element
from models.rune_circle import RuneCircle

DEFAULT_WEIGHT = 1.0


class Recipe:
    def __init__(self):
        self.components = defaultdict(float)

    def add(self, element: Element, amount: float = 1.0):
        self.components[element] += amount

    def normalize(self) -> Dict[Element, float]:
        total = sum(self.components.values())
        if total == 0:
            return {el: 0.0 for el in self.components}
        return {el: round(val / total, 3) for el, val in self.components.items()}

    def summary(self) -> Dict[str, float]:
        return {el.name: round(amt, 2) for el, amt in self.components.items()}

    def vector(self) -> Dict[Element, float]:
        return self.normalize()

    def to_prompt(self) -> str:
        norm = self.normalize()
        sorted_elements = sorted(norm.items(), key=lambda x: -x[1])
        parts = [f"{el.name} {int(weight * 100)}%" for el, weight in sorted_elements if weight > 0.01]
        return ", ".join(parts)


def build_recipe_from_circle(circle: RuneCircle) -> Recipe:
    recipe = Recipe()

    if circle.core:
        recipe.add(circle.core.element, 2.0)

    for level, sigils in circle.layers.items():
        for sigil in sigils:
            if sigil:
                level_weight = 1.0 / (level + 1)
                recipe.add(sigil.element, level_weight)

    return recipe
