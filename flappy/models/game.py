from typing import Any, Optional, List, Tuple
from PIL import Image
import numpy as np

from attr import attrs, attrib
import pygame
from flappy.utils.cords import distance_between_objects

from flappy.config.configuration import SCREEN_HEIGHT, SCREEN_WIDTH
from flappy.enums.actions import Actions
from flappy.enums.pipe_types import PipeTypes
from flappy.models.moving_block import MovingBlock
from flappy.models.pipe_sprite import PipeSprite
from flappy.models.player import Player
from pygame.surfarray import array3d
from collections import deque
import random


ADD_PIPES = pygame.USEREVENT + 1



@attrs(auto_attribs=True)
class Game:
    _screen: Any = attrib(init=False)
    _player: Optional[Player] = attrib(init=False)
    _all_sprites: pygame.sprite.Group = attrib(init=False)
    _enemies: pygame.sprite.Group = attrib(init=False)
    _step_counter: int = 0
    _history: deque = deque(maxlen=4)

    _running: bool = False


    def action_space(self) -> List[Actions]:
        return [Actions.NOTHING, Actions.JUMP]

    def _generate_pipe_pair(self) -> None:
        offset = random.randint(-1 * (SCREEN_HEIGHT*.4),SCREEN_HEIGHT*.4)

        top_p = PipeSprite(
            SCREEN_HEIGHT,
            50,
            (SCREEN_WIDTH, offset-50),
            3,
            type=PipeTypes.UPPER,
        )
        bottom_p = PipeSprite(
            SCREEN_HEIGHT,
            50,
            (SCREEN_WIDTH, SCREEN_HEIGHT+offset+50),
            3,
            type=PipeTypes.LOWER,
        )
        self._all_sprites.add(top_p, bottom_p)
        self._enemies.add(top_p, bottom_p)

    def setup(self):
        pygame.init()
        self._screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self._player = Player()
        self._all_sprites = pygame.sprite.Group()
        self._enemies = pygame.sprite.Group()

        ceiling = MovingBlock(9, SCREEN_WIDTH, (SCREEN_WIDTH/2, 0), 0)
        floor = MovingBlock(9, SCREEN_WIDTH, (SCREEN_WIDTH/2, SCREEN_HEIGHT), 0)
        self._enemies.add(ceiling, floor)
        self._all_sprites.add(ceiling, floor, self._player)

        self._generate_pipe_pair()


    def teardown(self):
        pygame.quit()

    def reset(self):
        pass

    def step(self, action: Actions) -> Tuple[pygame.surfarray.pixels3d, int, bool]:
        self._step_counter += 1
        """
        One in game step, this should return the state of the
        game and if its over or not.
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        if self._step_counter % 150 == 0:
            self._generate_pipe_pair()

        self._screen.fill((0, 0, 0))

        self._player.update(action=action)
        self._enemies.update()

        for e in self._all_sprites:
            self._screen.blit(e.surf, e.rect)


        terminal = False
        if pygame.sprite.spritecollideany(self._player, self._enemies):
            terminal = True

        def get_pipe_cord():
            # top location of the closest lower pipe

            for x in [x for x in self._enemies if type(x) is PipeSprite and x.type is PipeTypes.LOWER]:
                if self._player.rect.left > x.rect.topright[0]:
                    continue
                print(x.rect.topright)
                return x.rect.top
            raise Exception

        pygame.draw.line(self._screen, (255,0,0), (0, self._player.rect.bottom), (100, self._player.rect.bottom))
        pygame.draw.line(self._screen, (255,0,0), (0, get_pipe_cord()), (100, get_pipe_cord()))
        # updates the screen
        pygame.display.flip()

        while len(self._history) < 4:
            self._history.append(
                np.array([self._player.rect.bottom, get_pipe_cord()])
            )


        self._history.append(
            np.array([self._player.rect.bottom, get_pipe_cord()])
        )


        """
        image = array3d(pygame.display.get_surface())
        image = Image.fromarray(image)
        image = np.array(image.convert('L'))

        while len(self._screen_history) < 4:
            self._screen_history.append(np.zeros(image.shape))
        self._screen_history.append(image)
        #image = image[::8, ::8]
        #image = np.mean(image, axis=2).astype(np.uint8)
        image = np.stack(np.array(self._screen_history), axis=2)
        #import matplotlib.pyplot as plt
        #plt.imshow(image)
        #plt.show()
        #image = np.resize(image, (1, 125, 63))
        #image = Image.fromarray(image)
        #image = np.array(image.convert('L'))
        #image = ((image>128)*255).astype(np.uint8)
        """
        state = np.array(list(self._history)).flatten()
        """
        array([[230.        , 230.        , 230.        , 230.        ],
       [240.        , 240.        , 240.        , 240.        ],
       [460.        , 460.        , 460.        , 460.        ],
       [339.41125497, 339.41125497, 339.41125497, 339.41125497],
       [325.26911935, 325.26911935, 325.26911935, 325.26911935]])
        """

        return (state, -1 if terminal else 1, terminal)


