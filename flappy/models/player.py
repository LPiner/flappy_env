import pygame

from flappy.config.configuration import SCREEN_HEIGHT, SCREEN_WIDTH
from flappy.enums.actions import Actions


class Player(pygame.sprite.Sprite):
    def __init__(self, center=None):
        super(Player, self).__init__()
        if not center:
           center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(
            center=center
        )
        self.velocity = 0

    def update(self, action: Actions):
        if action is Actions.JUMP:
            self.rect.move_ip(0, -15)
        elif action is Actions.NOTHING:
            self.rect.move_ip(0, 5)


