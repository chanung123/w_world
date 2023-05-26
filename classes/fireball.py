import pygame


# Fireball 객체 정의
class Fireball(pygame.sprite.Sprite):
    """파이어볼"""

    def __init__(self, pos, vel, fireball_images):
        super().__init__()
        self.fireball_images = fireball_images
        self.image = fireball_images[0]
        self.rect = self.image.get_rect(center=pos)
        self.vel = vel

    def update(self):
        """Fireball 이동 및 스프라이트 이미지 갱신"""
        self.rect.move_ip(self.vel)
        sprite_index = int(pygame.time.get_ticks() / 100) % len(self.fireball_images)
        self.image = self.fireball_images[sprite_index]