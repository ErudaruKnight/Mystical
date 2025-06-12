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
RADIUS_STEP = 70
ANGLE_OFFSET = -math.pi / 2

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
    """Return combination of sigils along the main line."""
    parts = []
    for level in range(1, 6):
        sigil = circle.layers[level][0]
        parts.append(sigil.element.value if sigil else "empty")
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

    desc = {
        "Название": "Нажми кнопку",
        "Эффект": "для генерации описания заклинания",
        "Редкость": "-",
        "Пропорции": "-"
    }

    running = True
    while running:
        screen.fill((30, 30, 30))

        if circle.core:
            draw_sigil(screen, *CENTER, circle.core.element)

        for level in range(1, 6):
            radius = level * RADIUS_STEP + 100
            pygame.draw.circle(screen, (60, 60, 60), CENTER, radius, 1)

        max_r = 5 * RADIUS_STEP + 100
        start_line = (
            CENTER[0] + max_r * math.cos(ANGLE_OFFSET),
            CENTER[1] + max_r * math.sin(ANGLE_OFFSET),
        )
        end_line = (
            CENTER[0] - max_r * math.cos(ANGLE_OFFSET),
            CENTER[1] - max_r * math.sin(ANGLE_OFFSET),
        )
        pygame.draw.line(screen, (80, 80, 80), start_line, end_line, 2)

        for level, sigils in circle.layers.items():
            radius = level * RADIUS_STEP + 100
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

        eff = calculate_efficiency(circle)
        eff_text = font.render(f"Эффективность: {int(eff * 100)}%", True, (255, 255, 255))
        screen.blit(eff_text, (20, 20))

        name_text = font.render(desc.get("Название", "??"), True, (255, 255, 0))
        effect_text = font.render(desc.get("Эффект", "??"), True, (180, 180, 255))
        rarity_text = font.render(f"Редкость: {desc.get('Редкость', '-')}", True, (255, 180, 180))
        prompt_text = font.render(desc.get("Пропорции", ""), True, (200, 200, 200))

        screen.blit(name_text, (20, 50))
        screen.blit(effect_text, (20, 80))
        screen.blit(rarity_text, (20, 110))
        screen.blit(prompt_text, (20, 140))

        # Кнопка генерации
        generate_button = pygame.Rect(1440, 500, 200, 50)
        pygame.draw.rect(screen, (100, 100, 255), generate_button)
        button_text = font.render("Сгенерировать", True, (255, 255, 255))
        screen.blit(button_text, (generate_button.x + 10, generate_button.y + 10))

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
                        name, descr = spell
                        desc = {"Название": name, "Эффект": descr, "Редкость": "-", "Пропорции": combo}
                    else:
                        desc = {"Название": "Неизвестно", "Эффект": "Комбинация не найдена", "Редкость": "-", "Пропорции": combo}
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_element:
                    mx, my = pygame.mouse.get_pos()
                    dx = mx - CENTER[0]
                    dy = my - CENTER[1]
                    dist = math.hypot(dx, dy)
                    for level in range(1, 6):
                        radius = level * RADIUS_STEP + 100
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
