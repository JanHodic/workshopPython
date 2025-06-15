import pygame

from Player import Player
from enemy import Enemy
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


    # fce které interagují s pygame!
    score = 0

    ## Start pygame + start modulů!
    pygame.init()
    pygame.mixer.init()

    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)

    # Grafika!

    # Definice spritu

    font = pygame.font.SysFont(None, 32)
    score_font = pygame.font.SysFont(None, 28)
    # Nastaveni okna aj.
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Running Game")


    # hodiny - FPS CLOCK / heart rate
    clock = pygame.time.Clock()
    layers = init_layers()

    # časový interval nového enemy
    enemy_spawn_timer = 0
    enemy_spawn_interval = 5000

    # Kolecke spritů
    my_sprites = pygame.sprite.Group()
    scroll_enabled = False
    start_ticks = pygame.time.get_ticks()

    # start:
    running = True

    human = Human(mass=50, width=50, height=100)
    world = World(elasticity_coeff=0.9, ground=400, velocity=3.0)
    game = GameProcess(human=human, world=world, time_step=1 / 45)
    player = Player(game, x=100, y=490)
    player.game.clock = clock  # předání clock do playera
    player.game.screen = screen  # předání screen (kvůli clamp_ip)

    my_sprites.add(player)

    # enemy
    enemy = Enemy(x=WIDTH + 50, y=world.ground + 110)  # Spustí se mimo obrazovku zprava
    my_sprites.add(enemy)


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
        score_text = score_font.render(f"Score: {score}", True, BLACK)

        enemy_spawn_timer += clock.get_time()
        if enemy_spawn_timer > enemy_spawn_interval:
            enemy = Enemy(x=WIDTH + 50, y=world.ground + 110)
            my_sprites.add(enemy)
            enemy_spawn_timer = 0
        # Update
        for sprite in my_sprites:
            if hasattr(sprite, "update"):
                if isinstance(sprite, Enemy):
                    sprite.update(scroll_enabled)
                else:
                    sprite.update()
                if isinstance(sprite, Enemy) and not sprite.scored:
                    if sprite.rect.right < player.rect.left:
                        score += 1
                        sprite.scored = True

        # Render

        screen.fill(BLACK)
        draw_parallax_background(screen, layers, scroll_enabled)
        my_sprites.draw(screen)
        screen.blit(time_text, (30, 30))
        screen.blit(score_text, (30, 60))

        pygame.display.flip()

    pygame.quit()
