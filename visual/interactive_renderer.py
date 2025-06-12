import pygame
import math
from models.rune_circle import RuneCircle
from models.sigil import Sigil
from models.elements import Element
from logic.efficiency import calculate_efficiency
from logic.spell_db import get_spell, populate_basic_spells

WIDTH, HEIGHT = 1920, 1080
CIRCLE_AREA_WIDTH = 1200
CENTER = (CIRCLE_AREA_WIDTH // 2, HEIGHT // 2)
# Slightly larger circle for a more impressive ritual look
RADIUS_STEP = 90
BASE_RADIUS = 150
ANGLE_OFFSET = -math.pi / 2
DECOR_COLOR = (80, 60, 120)

COLOR_MAP = {
    Element.FIRE: (255, 80, 0),
    Element.WATER: (0, 120, 255),
    Element.AIR: (200, 200, 200),
    Element.EARTH: (80, 180, 80),
}

def draw_socket(screen, x, y, highlight=False):
    color = (100, 100, 100) if not highlight else (0, 255, 0)
    pygame.draw.circle(screen, color, (int(x), int(y)), 20, 2)

def draw_sigil(screen, x, y, element: Element):
    color = COLOR_MAP[element]
    if element == Element.FIRE:
        pygame.draw.polygon(screen, color, [(x, y - 15), (x - 15, y + 10), (x + 15, y + 10)])
    elif element == Element.WATER:
        pygame.draw.circle(screen, color, (x, y), 15)
    elif element == Element.EARTH:
        pygame.draw.rect(screen, color, pygame.Rect(x - 15, y - 15, 30, 30))
    elif element == Element.AIR:
        pygame.draw.polygon(screen, color, [(x, y - 15), (x - 15, y), (x, y + 15), (x + 15, y)])

def current_combo(circle: RuneCircle) -> str:
    """Return elements from the single ring starting at the guideline."""
    sigils = circle.layers[1]
    parts = [s.element.value if s else "empty" for s in sigils]
    return "-".join(parts)

def interactive_render(circle: RuneCircle):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rune Circle - Interactive")
    font = pygame.font.SysFont("Arial", 24)
    clock = pygame.time.Clock()
    populate_basic_spells()

    dragging_element = None
    mouse_pos = (0, 0)

    library_positions = {
        Element.FIRE: (1450, 150),
        Element.WATER: (1450, 230),
        Element.AIR: (1450, 310),
        Element.EARTH: (1450, 390),
    }

    default_desc = {
        "Название": "Нажми кнопку",
        "Эффект": "для генерации описания заклинания",
        "Эффективность": "-",
        "Пропорции": "-"
    }
    desc = dict(default_desc)

    running = True
    while running:
        screen.fill((30, 30, 30))

        if circle.core:
            draw_sigil(screen, *CENTER, circle.core.element)

        for level in range(1, 2):
            radius = level * RADIUS_STEP + BASE_RADIUS
            pygame.draw.circle(screen, DECOR_COLOR, CENTER, radius, 3)
            pygame.draw.circle(screen, DECOR_COLOR, CENTER, radius + 30, 1)
            pygame.draw.circle(screen, DECOR_COLOR, CENTER, radius - 30, 1)

            inner_r = 0
            outer_r = radius
            start_line = (
                CENTER[0] + inner_r * math.cos(ANGLE_OFFSET),
                CENTER[1] + inner_r * math.sin(ANGLE_OFFSET),
            )
            end_line = (
                CENTER[0] + outer_r * math.cos(ANGLE_OFFSET),
                CENTER[1] + outer_r * math.sin(ANGLE_OFFSET),
            )
            pygame.draw.line(screen, DECOR_COLOR, start_line, end_line, 2)

            pygame.draw.line(screen, DECOR_COLOR, (CENTER[0] - radius, CENTER[1]), (CENTER[0] + radius, CENTER[1]), 1)
            pygame.draw.line(screen, DECOR_COLOR, (CENTER[0], CENTER[1] - radius), (CENTER[0], CENTER[1] + radius), 1)

            # Decorative spokes and pentagon to resemble a ritual circle
            points = []
            for i in range(5):
                ang = math.radians(72 * i) + ANGLE_OFFSET
                px = CENTER[0] + radius * math.cos(ang)
                py = CENTER[1] + radius * math.sin(ang)
                points.append((px, py))
                pygame.draw.line(screen, DECOR_COLOR, CENTER, (px, py), 1)
            pygame.draw.polygon(screen, DECOR_COLOR, points, 1)
            for i in range(5):
                pygame.draw.line(screen, DECOR_COLOR, points[i], points[(i + 2) % 5], 1)

        for level, sigils in circle.layers.items():
            radius = level * RADIUS_STEP + BASE_RADIUS
            for i in range(5):
                angle = math.radians((360 / 5) * i) + ANGLE_OFFSET
                x = CENTER[0] + radius * math.cos(angle)
                y = CENTER[1] + radius * math.sin(angle)

                highlight = False
                if dragging_element:
                    mx, my = mouse_pos
                    if math.hypot(mx - x, my - y) < 25:
                        highlight = True

                draw_socket(screen, x, y, highlight)

                sigil = sigils[i]
                if sigil:
                    draw_sigil(screen, int(x), int(y), sigil.element)

        pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(CIRCLE_AREA_WIDTH, 0, WIDTH - CIRCLE_AREA_WIDTH, HEIGHT))
        for elem, pos in library_positions.items():
            draw_sigil(screen, *pos, elem)
            text = font.render(elem.name, True, (255, 255, 255))
            screen.blit(text, (pos[0] + 30, pos[1] - 10))

        if dragging_element:
            draw_sigil(screen, *mouse_pos, dragging_element)

        current_eff = calculate_efficiency(circle)
        eff_display = desc.get("Эффективность", "-")
        if eff_display == "-":
            eff_display = str(int(current_eff * 100))
        eff_text = font.render(f"Эффективность: {eff_display}%", True, (255, 255, 255))
        screen.blit(eff_text, (20, 20))

        name_text = font.render(desc.get("Название", "??"), True, (255, 255, 0))
        effect_text = font.render(desc.get("Эффект", "??"), True, (180, 180, 255))
        prompt_text = font.render(desc.get("Пропорции", ""), True, (200, 200, 200))

        screen.blit(name_text, (20, 50))
        screen.blit(effect_text, (20, 80))
        screen.blit(prompt_text, (20, 110))

        # Кнопки управления
        generate_button = pygame.Rect(1440, 500, 200, 50)
        reset_button = pygame.Rect(1440, 560, 200, 50)

        pygame.draw.rect(screen, (100, 100, 255), generate_button)
        pygame.draw.rect(screen, (180, 60, 60), reset_button)

        button_text = font.render("Сгенерировать", True, (255, 255, 255))
        reset_text = font.render("Сброс", True, (255, 255, 255))
        screen.blit(button_text, (generate_button.x + 10, generate_button.y + 10))
        screen.blit(reset_text, (reset_button.x + 65, reset_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for elem, (lx, ly) in library_positions.items():
                    if abs(mx - lx) < 20 and abs(my - ly) < 20:
                        dragging_element = elem
                        break
                if generate_button.collidepoint((mx, my)):
                    combo = current_combo(circle)
                    spell = get_spell(combo)
                    if spell:
                        name, descr, eff = spell
                        desc = {
                            "Название": name,
                            "Эффект": descr,
                            "Эффективность": str(int(eff * 100)),
                            "Пропорции": combo,
                        }
                    else:
                        desc = {
                            "Название": "Неизвестно",
                            "Эффект": "Комбинация не найдена",
                            "Эффективность": str(int(calculate_efficiency(circle) * 100)),
                            "Пропорции": combo,
                        }
                elif reset_button.collidepoint((mx, my)):
                    circle.clear()
                    desc = dict(default_desc)
                    dragging_element = None
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_element:
                    mx, my = pygame.mouse.get_pos()
                    dx = mx - CENTER[0]
                    dy = my - CENTER[1]
                    dist = math.hypot(dx, dy)
                    for level in range(1, 2):
                        radius = level * RADIUS_STEP + BASE_RADIUS
                        if abs(dist - radius) < 20:
                            angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360
                            adjusted = (angle - math.degrees(ANGLE_OFFSET)) % 360
                            position = int((adjusted + 36) // 72) % 5
                            circle.add_sigil(Sigil(dragging_element, level=level, position=position))
                            break
                    dragging_element = None
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
