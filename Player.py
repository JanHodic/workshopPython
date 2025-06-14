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

        self.speed = 5
        self.anim_timer = 0
        self.anim_interval = 100

        self.velocity = pygame.Vector2(0, 0)

    def load_first_row_frames(self):
        return [
            self.sprite_sheet.subsurface(
                pygame.Rect(col * self.frame_width, 3 * self.frame_height, self.frame_width, self.frame_height)
            ) for col in range(self.columns)
        ]

    def update(self):
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            moved = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            moved = True

        if moved:
            self.anim_timer += self.game.clock.get_time()
            if self.anim_timer > self.anim_interval:
                self.anim_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]
        else:
            self.frame_index = 0
            self.image = self.frames[self.frame_index]

        # Omez pohyb v rámci obrazovky
        self.rect.clamp_ip(pygame.Rect(0, 0, self.game.screen.get_width(), self.game.screen.get_height()))