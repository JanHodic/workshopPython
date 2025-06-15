import pygame
import sys
from enemy import Enemy
from background.bg import init_layers, draw_parallax_background

def home_screen():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Welcome")
    start_time = pygame.time.get_ticks()

    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)

    # Barvy
    BLUE = (50, 100, 200)
    GRAY = (60, 60, 60)
    WHITE = (255, 255, 255)
    DARK = (20, 20, 50)
    GREEN = (0, 200, 0)

    layers = init_layers()

    title_font = pygame.font.SysFont(None, 72)
    font = pygame.font.SysFont(None, 28)

    title_text = title_font.render("RUNNING GAME", True, DARK)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 200))
    settings_text = title_font.render("SETTINGS", True, DARK)
    settings_rect = settings_text.get_rect(center=(WIDTH // 2, 200))

    difficulty = "beginner"
    current_menu = "home"

    # Načti a zmenši obrázek ovládání
    controls_img_original = pygame.image.load("assets/navigation.png").convert_alpha()
    controls_img = pygame.transform.scale(controls_img_original, (150, 150))
    controls_rect = controls_img.get_rect(topright=(WIDTH /2 + 100, HEIGHT /2))  # 20 px od pravého a horního okraje
    home_image = pygame.image.load("assets/uvod.png").convert_alpha()
    home_rect = home_image.get_rect(topleft=(0,0))

    # Tlačítka
    buttons_home = [
        {"label": "START", "action": "start"},
        {"label": "SETTINGS", "action": "settings"},
        {"label": "EXIT GAME", "action": "quit"},
    ]
    buttons_settings = [
        {"label": "BEGINNER", "value": "beginner"},
        {"label": "EXPERT", "value": "expert"},
        {"label": "START GAME", "action": "start"},
    ]

    def create_button_rects(buttons, y_offset):
        button_rects = []
        button_width, button_height = 160, 50
        spacing = 30
        total_width = len(buttons) * button_width + (len(buttons) - 1) * spacing
        start_x = (WIDTH - total_width) // 2
        y = HEIGHT - button_height - y_offset
        for i, btn in enumerate(buttons):
            x = start_x + i * (button_width + spacing)
            rect = pygame.Rect(x, y, button_width, button_height)
            button_rects.append((rect, btn))
        return button_rects

    running = True
    while running:
        screen.fill(WHITE)
        draw_parallax_background(screen, layers, scroll_enabled=False)

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time


        mouse_pos = pygame.mouse.get_pos()
        cursor_handled = False

        if elapsed_time > 5000:
            if current_menu == "home":
                button_rects = create_button_rects(buttons_home, 100)
                screen.blit(title_text, title_rect)
            else:
                button_rects = create_button_rects(buttons_settings, 100)
                screen.blit(settings_text, settings_rect)
        else:
            button_rects = []  # žádné tlačítka před uplynutím času
            # Vykresli obrázek ovládání
            screen.blit(home_image, home_rect)
            screen.blit(controls_img, controls_rect)


        # Vykreslení tlačítek
        for rect, btn in button_rects:
            color = GRAY
            if "value" in btn and btn["value"] == difficulty:
                color = GREEN  # zvýrazni aktivní obtížnost
            pygame.draw.rect(screen, color, rect)
            text = font.render(btn["label"], True, WHITE)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
            if rect.collidepoint(mouse_pos):
                cursor_handled = True

        # Cursor
        if cursor_handled:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()

        # Eventy
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and current_menu == "home":
                    return "start", difficulty
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, btn in button_rects:
                    if rect.collidepoint(event.pos):
                        if current_menu == "home":
                            if btn["action"] == "start":
                                return "start", difficulty
                            elif btn["action"] == "settings":
                                current_menu = "settings"
                            elif btn["action"] == "quit":
                                pygame.quit()
                                sys.exit()
                        elif current_menu == "settings":
                            if "value" in btn:
                                difficulty = btn["value"]
                            elif btn.get("action") == "start":
                                return "start", difficulty