import pygame

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


    # Nastaveni okna aj.
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Running Game")


    # hodiny - FPS CLOCK / heart rate
    clock = pygame.time.Clock()
    layers = init_layers()

    # Kolecke spritů
    my_sprites = pygame.sprite.Group()
    scroll_enabled = False
    # start:
    running = True

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
                    scroll_enabled = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    scroll_enabled = False

        # Update
        my_sprites.update()

        # Render
        screen.fill(BLACK)
        my_sprites.draw(screen)
        draw_parallax_background(screen, layers, scroll_enabled)
        pygame.display.flip()

    pygame.quit()
