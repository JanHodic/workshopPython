import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, clock):
        super().__init__()
        self.sprite_sheet = pygame.image.load("assets/boom.png").convert_alpha()
        self.frame_width = self.sprite_sheet.get_width() // 7  # 7 snímků
        self.frame_height = self.sprite_sheet.get_height()
        self.clock = clock
        self.frames = [
            self.sprite_sheet.subsurface(pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height))
            for i in range(7)
        ]

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.anim_timer = 0
        self.anim_interval = 80  # rychlost animace

    def update(self):
        self.anim_timer += self.clock.get_time()
        if self.anim_timer > self.anim_interval:
            self.anim_timer = 0
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.frame_index]