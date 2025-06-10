import math
import pygame
from models.elements import Element
from models.rune_circle import RuneCircle
from logic.efficiency import compute_efficiency


WINDOW_SIZE = 800
CENTER = (WINDOW_SIZE // 2, WINDOW_SIZE // 2)
LEVEL_DISTANCE = 70
SIGIL_SIZE = 15


def _get_position(level: int, position: int) -> tuple[int, int]:
    if level == 0:
        return CENTER
    angle = 2 * math.pi / RuneCircle.SLOTS * position
    radius = LEVEL_DISTANCE * level
    x = CENTER[0] + radius * math.cos(angle)
    y = CENTER[1] + radius * math.sin(angle)
    return int(x), int(y)


def _draw_sigil(screen: pygame.Surface, element: Element, pos: tuple[int, int]) -> None:
    x, y = pos
    if element == Element.FIRE:
        color = (255, 0, 0)
        points = [(x, y - SIGIL_SIZE), (x - SIGIL_SIZE, y + SIGIL_SIZE), (x + SIGIL_SIZE, y + SIGIL_SIZE)]
        pygame.draw.polygon(screen, color, points)
    elif element == Element.WATER:
        color = (0, 0, 255)
        pygame.draw.circle(screen, color, pos, SIGIL_SIZE)
    elif element == Element.AIR:
        color = (200, 200, 200)
        points = [
            (x, y - SIGIL_SIZE),
            (x - SIGIL_SIZE, y),
            (x, y + SIGIL_SIZE),
            (x + SIGIL_SIZE, y),
        ]
        pygame.draw.polygon(screen, color, points)
    elif element == Element.EARTH:
        color = (0, 255, 0)
        rect = pygame.Rect(x - SIGIL_SIZE, y - SIGIL_SIZE, SIGIL_SIZE * 2, SIGIL_SIZE * 2)
        pygame.draw.rect(screen, color, rect)


def render_circle(circle: RuneCircle) -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Rune Circle")
    font = pygame.font.SysFont(None, 24)
    efficiency = compute_efficiency(circle)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((20, 20, 20))
        for level, slots in circle.levels.items():
            for pos_index, sigil in slots.items():
                pos = _get_position(level, pos_index)
                _draw_sigil(screen, sigil.element, pos)

        text = font.render(f"\u042d\u0444\u0444\u0435\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u044c: {int(efficiency)}%", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()

    pygame.quit()
