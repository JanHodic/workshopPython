import pygame
from math_operations.models.human import Human
from math_operations.models.world import World
from business_logic.game_process import GameProcess

from background.bg import draw_parallax_background, init_layers


def run_game():
    # konstanty a fce které neinteragují s pygame!
    BLACK = (0, 0, 0)
    PURPLE = (150, 10, 100)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)

    WIDTH = 800
    HEIGHT = 600
    FPS = 60


    # Nastav název okna
    pygame.display.set_caption("Moje Pygame aplikace")
    # fce které interagují s pygame!


    ## Start pygame + start modulů!
    pygame.init()
    pygame.mixer.init()

    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)

    # Grafika!

    # Definice spritu

    font = pygame.font.SysFont(None, 32)
    # Nastaveni okna aj.
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Running Game")


    # hodiny - FPS CLOCK / heart rate
    clock = pygame.time.Clock()
    layers = init_layers()

    # Kolecke spritů
    my_sprites = pygame.sprite.Group()
    scroll_enabled = False
    start_ticks = pygame.time.get_ticks()

    # start:
    running = True

    human = Human(mass=50, width=50, height=100)
    world = World(elasticity_coeff=0.9, ground=400, velocity=3.0)
    game = GameProcess(human=human, world=world, time_step=1 / 45)

    # cyklus udrzujici okno v chodu
    while running:
        # FPS kontrola / jeslti bezi dle rychlosti!
        clock.tick(FPS)


        # Event
        for event in pygame.event.get():
            # print(event) - pokud potrebujete info co se zmacklo.
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    game.change_velocity(5)
                    scroll_enabled = True
                elif event.key == pygame.K_LEFT:
                    game.change_velocity(-5)
                elif event.key == pygame.K_SPACE:
                    print("klavesa")
                    game.jump(jump_velocity=10)  # hodnota dle potřeby

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    scroll_enabled = False
                elif event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    game.change_velocity(0)  # zastaví horizontální pohyb

        # Výpočet času
        elapsed_ms = pygame.time.get_ticks() - start_ticks
        total_seconds = elapsed_ms / 1000
        minutes = int(total_seconds) // 60
        seconds = int(total_seconds) % 60
        tenths = int((total_seconds - int(total_seconds)) * 10)

        time_text = font.render(f"Time: {minutes:02}:{seconds:02}.{tenths}", True, BLACK)
        # Update
        my_sprites.update()

        # Render
        screen.fill(BLACK)
        my_sprites.draw(screen)
        draw_parallax_background(screen, layers, scroll_enabled)
        screen.blit(time_text, (30, 30))
        pygame.display.flip()

    pygame.quit()
