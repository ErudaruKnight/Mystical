from enum import Enum

class Element(Enum):
    FIRE = "fire"
    WATER = "water"
    AIR = "air"
    EARTH = "earth"

synergy_map = {
    (Element.WATER, Element.AIR): +0.20,
    (Element.FIRE, Element.EARTH): +0.10,
    (Element.FIRE, Element.AIR): +0.15,
    (Element.WATER, Element.EARTH): +0.10,
    (Element.WATER, Element.FIRE): -0.30,
    (Element.EARTH, Element.AIR): -0.20,
}

def get_interaction_bonus(e1: Element, e2: Element) -> float:
    if (e1, e2) in synergy_map:
        return synergy_map[(e1, e2)]
    elif (e2, e1) in synergy_map:
        return synergy_map[(e2, e1)]
    return 0.0
