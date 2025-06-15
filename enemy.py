import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=3):
        super().__init__()

        self.sprite_sheet = pygame.image.load("assets/enemy_plant.png").convert_alpha()
        self.frame_width = self.sprite_sheet.get_width() // 2
        self.frame_height = self.sprite_sheet.get_height()
        self.frames = [
            self.sprite_sheet.subsurface(pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height))
            for i in range(2)
        ]

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.speed = speed
        self.anim_timer = 0
        self.anim_interval = 1300  # ms – mění snímek každých 0.3 sekundy

        self.scored = False

    def update(self, scroll_enabled=True):
        if scroll_enabled:
            self.rect.x -= self.speed

        # Animace běží stále
        self.anim_timer += pygame.time.get_ticks() % 1000
        if self.anim_timer > self.anim_interval:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

        if self.rect.right < 0:
            self.kill()

