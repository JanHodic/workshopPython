import pygame

from Player import Player
from enemy import Enemy
from math_operations.models.human import Human
from math_operations.models.world import World
from business_logic.game_process import GameProcess
from explosion import Explosion

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
    lives = 5
    game_over = False

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
    scroll_enabled = True
    start_ticks = pygame.time.get_ticks()

    # start:
    running = True

    human = Human(mass=50, width=50, height=100)
    world = World(elasticity_coeff=0.9, ground=400, velocity=3.0)
    game = GameProcess(human=human, world=world, time_step=1 / 45)
    player = Player(game, x=100, y=490)
    player.game.clock = clock  # předání clock do playera
    player.game.screen = screen  # předání screen (kvůli clamp_ip)
    explosions_group = pygame.sprite.Group()
    my_sprites.add(player)
    # enemy
    enemy = Enemy(x=WIDTH + 50, y=HEIGHT - 85)  # Spustí se mimo obrazovku zprava
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
                    game.jump(jump_velocity=10)  # hodnota dle potřeby

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    scroll_enabled = True
                elif event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    game.change_velocity(5)  # zastaví horizontální pohyb

        # Výpočet času
        elapsed_ms = pygame.time.get_ticks() - start_ticks
        total_seconds = elapsed_ms / 1000
        minutes = int(total_seconds) // 60
        seconds = int(total_seconds) % 60
        tenths = int((total_seconds - int(total_seconds)) * 10)

        time_text = font.render(f"Time: {minutes:02}:{seconds:02}.{tenths}", True, BLACK)
        score_text = score_font.render(f"Points: {score}", True, BLACK)
        lives_text = score_font.render(f"Lives: {lives}", True, BLACK)

        enemy_spawn_timer += clock.get_time()
        if enemy_spawn_timer > enemy_spawn_interval:
            enemy = Enemy(x=WIDTH + 50, y=HEIGHT - 85)
            my_sprites.add(enemy)
            enemy_spawn_timer = 0

        # Update
        for sprite in my_sprites:
            if hasattr(sprite, "update"):
                if isinstance(sprite, Enemy):
                    sprite.update(scroll_enabled)
                else:
                    sprite.update()

            # Kolize mezi Enemy a Player
            if isinstance(sprite, Enemy) and not sprite.scored:
                if sprite.rect.colliderect(player.rect):
                    explosion = Explosion(sprite.rect.centerx, sprite.rect.centery, clock)
                    explosions_group.add(explosion)
                    my_sprites.remove(sprite)  # Odstraníme kolidujícího enemy
                    lives -= 1
                    sprite.scored = True
                    if lives <= 0:
                        running = False
                        game_over = True

                elif sprite.rect.right < player.rect.left:
                    score += 1
                    sprite.scored = True


        if game_over:
            game_over_font = pygame.font.SysFont(None, 72)
            small_font = pygame.font.SysFont(None, 36)

            game_over_text = game_over_font.render("GAME OVER", True, RED)
            final_score_text = small_font.render(f"Points: {score}", True, BLACK)
            final_time_text = small_font.render(f"Time: {minutes:02}:{seconds:02}.{tenths}", True, BLACK)
            restart_text = small_font.render("Press SPACE to Restart or ESC to Quit", True, BLACK)

            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
            score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
            time_rect = final_time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))

            screen.fill(BLACK)
            draw_parallax_background(screen, layers, False)
            screen.blit(game_over_text, text_rect)
            screen.blit(final_score_text, score_rect)
            screen.blit(final_time_text, time_rect)
            screen.blit(restart_text, restart_rect)
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            waiting = False  # restart
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return

        # Render

        screen.fill(BLACK)
        draw_parallax_background(screen, layers, scroll_enabled)
        my_sprites.draw(screen)
        explosions_group.update()
        explosions_group.draw(screen)
        screen.blit(time_text, (30, 30))
        screen.blit(score_text, (30, 60))
        screen.blit(lives_text, (30, 80))
        # === LADICÍ OBRYSY (obdélníky kolem sprite.rect) ===
        #for sprite in my_sprites:
         #   pygame.draw.rect(screen, (255, 0, 0), sprite.rect, 2)
        pygame.display.flip()

    pygame.quit()
