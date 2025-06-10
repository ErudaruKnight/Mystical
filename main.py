from models.elements import Element
from models.sigil import Sigil
from models.rune_circle import RuneCircle
from logic.efficiency import compute_efficiency
from visual.renderer import render_circle


def create_example_circle() -> RuneCircle:
    circle = RuneCircle()
    circle.add_sigil(Sigil(Element.FIRE, 0, 0))
    circle.add_sigil(Sigil(Element.AIR, 1, 0))
    circle.add_sigil(Sigil(Element.WATER, 1, 2))
    circle.add_sigil(Sigil(Element.EARTH, 2, 1))
    return circle


def main() -> None:
    circle = create_example_circle()
    efficiency = compute_efficiency(circle)
    print(
        (
            f"\u042d\u0444\u0444\u0435\u043a\u0442\u0438\u0432\u043d"
            f"\u043e\u0441\u0442\u044c: {efficiency:.0f}%"
        )
    )
    render_circle(circle)


if __name__ == "__main__":
    main()