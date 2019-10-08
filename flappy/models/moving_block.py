from typing import Tuple

import pygame

class MovingBlock(pygame.sprite.Sprite):

    def __init__(self, height: int, width: int, location: Tuple[int, int], speed: int):

        super(MovingBlock, self).__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=location
        )
        self.speed = speed

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()