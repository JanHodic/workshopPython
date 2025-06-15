import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.sprite_sheet = pygame.image.load("assets/player.png").convert_alpha()

        self.columns = 7
        self.frame_width = 1009 // 10
        self.frame_height = 95

        self.frames = self.load_first_row_frames()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

        # Rychlosti
        self.walk_speed = 5
        self.run_speed = 9
        self.jump_strength = -25    # záporné = skok nahoru
        self.gravity = 0.8

        # Stav
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = True       # zatím jednoduchý model (hrací plocha = spodní okraj)

        # Animace
        self.anim_timer = 0
        self.anim_interval = 100

    def load_first_row_frames(self):
        return [
            self.sprite_sheet.subsurface(
                pygame.Rect(col * self.frame_width, 3 * self.frame_height, self.frame_width, self.frame_height)
            ) for col in range(self.columns)
        ]

    def update(self):
        keys = pygame.key.get_pressed()
        moved = False

        # Zjisti, zda je stisknutý Shift
        running = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        speed = self.run_speed if running else self.walk_speed

        # Vodorovný pohyb
        if keys[pygame.K_LEFT]:
            self.rect.x -= speed
            moved = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += speed
            moved = True

        # Skok – jen pokud je na zemi
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity.y = self.jump_strength
            self.on_ground = False

        # Gravitace
        self.velocity.y += self.gravity
        self.rect.y += self.velocity.y

        # ZEM: ohraničení spodní hranou
        floor_y = self.game.screen.get_height() - self.rect.height + 30
        if self.rect.bottom >= floor_y:
            self.rect.bottom = floor_y
            self.velocity.y = 0
            self.on_ground = True

        # Animace
        if moved:
            self.anim_timer += self.game.clock.get_time()
            if self.anim_timer > self.anim_interval:
                self.anim_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]
        else:
            self.frame_index = 0
            self.image = self.frames[self.frame_index]

        # Omez pohyb v rámci obrazovky (X směr)
        self.rect.clamp_ip(pygame.Rect(0, 0, self.game.screen.get_width(), self.game.screen.get_height()))
