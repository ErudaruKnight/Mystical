from models.elements import Element
from models.sigil import Sigil
from models.rune_circle import RuneCircle
from visual.interactive_renderer import interactive_render

def main():
    circle = RuneCircle()
    ##circle.add_sigil(Sigil(Element.FIRE, level=0, position=0))
    interactive_render(circle)

if __name__ == "__main__":
    main()
