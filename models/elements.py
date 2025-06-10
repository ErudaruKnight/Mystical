from enum import Enum


class Element(Enum):
    FIRE = 'fire'
    WATER = 'water'
    AIR = 'air'
    EARTH = 'earth'


# Base synergy values between elements
_base_synergy = {
    (Element.WATER, Element.AIR): 0.20,
    (Element.FIRE, Element.EARTH): 0.10,
    (Element.FIRE, Element.AIR): 0.15,
    (Element.WATER, Element.EARTH): 0.10,
    (Element.WATER, Element.FIRE): -0.30,
    (Element.EARTH, Element.AIR): -0.20,
}

# Make the synergy map symmetrical
synergy_map = {}
for (el1, el2), value in _base_synergy.items():
    synergy_map[(el1, el2)] = value
    synergy_map[(el2, el1)] = value
