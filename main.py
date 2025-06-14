import pygame

from bacground.bg import draw_parallax_background

# konstanty a fce které neinteragují s pygame!
BLACK = (0, 0, 0)
PURPLE = (150, 10, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

WIDTH = 800
HEIGHT = 600
FPS = 45


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

layers = [
    {"image": pygame.image.load("src/images/layer-1.png").convert_alpha(), "speed": 0.2, "y": 0},
    {"image": pygame.image.load("src/images/layer-2.png").convert_alpha(), "speed": 0.5, "y": 100},
    {"image": pygame.image.load("src/images/layer-3.png").convert_alpha(), "speed": 1.0, "y": 0},
    {"image": pygame.image.load("src/images/layer-4.png").convert_alpha(), "speed": 2.0, "y": 100},
    {"image": pygame.image.load("src/images/layer-5.png").convert_alpha(), "speed": 3.0, "y": 100},
]


for layer in layers:
    layer["x1"] = 0
    layer["x2"] = layer["image"].get_width()

# hodiny - FPS CLOCK / heart rate
clock = pygame.time.Clock()

# Kolecke spritů
my_sprites = pygame.sprite.Group()

# start:
running = True

# cyklus udrzujici okno v chodu
while running:
    # FPS kontrola / jeslti bezi dle rychlosti!
    dt = clock.tick(FPS)

    # Event
    for event in pygame.event.get():
        # print(event) - pokud potrebujete info co se zmacklo.
        if event.type == pygame.QUIT:
            running = False

    # Update
    my_sprites.update()

    # Render
    screen.fill(BLACK)
    my_sprites.draw(screen)
    draw_parallax_background(screen, layers)
    pygame.display.flip()

pygame.quit()
