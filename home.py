import pygame
import sys

from background.bg import init_layers, draw_parallax_background


def home_screen():
    # Inicializace pygame
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Welcome")

    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)
    # Barvy
    BLUE = (50, 100, 200)
    WHITE = (255, 255, 255)
    layers = init_layers()

    # Tlačítko
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 40, 200, 80)

    # Font pro nápis na tlačítku
    font = pygame.font.SysFont(None, 48)
    text = font.render("START", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)

    running = True
    while running:
        screen.fill(WHITE)

        # Vykresli tlačítko
        draw_parallax_background(screen, layers, False)

        pygame.draw.rect(screen, BLUE, button_rect)
        screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True  # Spustí hru
    return False