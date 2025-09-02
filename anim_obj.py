from spritesheet import SpriteSheet

import pygame
from pygame import Surface
from pygame import Color as Colour

class AnimatedSprite(SpriteSheet):
    def __init__(self, file_path: str, columns: int, rows: int, position: tuple[int, int], colour_key: Colour = Colour(255, 0, 255),) -> None:
        SpriteSheet.__init__(self, file_path, columns, rows, colour_key)

        self.__anim_frames: int = 0
        self.__position = position


    def animate_next_frame(self, surface):
        self.blit(surface=surface, sprite_id=self.__anim_frames, position=self.__position)
        self.__anim_frames += 1

        if self.__anim_frames >= self.sprite_count():
            self.__anim_frames = -1

    def start_animation(self):
        self.__anim_frames = 0

    def update_position(self, new_position: tuple[int, int]):
        self.__position = new_position

    def get_frame(self):
        return self.__anim_frames
