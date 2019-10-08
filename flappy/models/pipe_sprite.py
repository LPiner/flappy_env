
import pygame
from flappy.models.moving_block import MovingBlock
from typing import Tuple
from flappy.enums.pipe_types import PipeTypes


class PipeSprite(MovingBlock):

    def __init__(self, height: int, width: int, location: Tuple[int, int], speed: int, type: PipeTypes):
        super(PipeSprite, self).__init__(height, width, location, speed)
        self.type = type
