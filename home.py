import pygame
import sys

from background.bg import init_layers, draw_parallax_background


def home_screen():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Welcome")

    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)

    # Barvy
    BLUE = (50, 100, 200)
    GRAY = (60, 60, 60)
    WHITE = (255, 255, 255)
    DARK = (20, 20, 50)
    layers = init_layers()

    title_font = pygame.font.SysFont(None, 72)  # Titulek
    font = pygame.font.SysFont(None, 28)

    title_text = title_font.render("RUNNING GAME", True, DARK)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 200))

    # Menu položky jako seznam dictů
    buttons = [
        {"label": "START", "action": "start"},
        {"label": "SETTINGS", "action": "settings"},
        {"label": "EXIT GAME", "action": "quit"},
    ]

    button_rects = []

    button_width, button_height = 160, 50
    spacing = 30
    total_width = len(buttons) * button_width + (len(buttons) - 1) * spacing
    start_x = (WIDTH - total_width) // 2
    y = HEIGHT - button_height - 100  # 40px odspodu

    # Vytvoření button rects
    for i, btn in enumerate(buttons):
        x = start_x + i * (button_width + spacing)
        rect = pygame.Rect(x, y, button_width, button_height)
        button_rects.append((rect, btn))

    running = True
    while running:
        screen.fill(WHITE)
        draw_parallax_background(screen, layers, scroll_enabled=False)

        # Vykresli titulek
        screen.blit(title_text, title_rect)
        mouse_pos = pygame.mouse.get_pos()
        cursor_handled = False

        # Tlačítka
        for rect, btn in button_rects:
            pygame.draw.rect(screen, GRAY, rect)
            text = font.render(btn["label"], True, WHITE)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
            if rect.collidepoint(mouse_pos):
                cursor_handled = True

        # Nastav kurzor jen jednou za frame
        if cursor_handled:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "start"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, btn in button_rects:
                    if rect.collidepoint(event.pos):
                        if btn["action"] == "start":
                            return "start"
                        elif btn["action"] == "settings":
                            return "settings"
                        elif btn["action"] == "quit":
                            pygame.quit()
                            sys.exit()