from spritesheet import SpriteSheet

# Creator of the original was british. I wanted to respect their decision, even though
# I disagree with it.
from pygame import Color as Colour

# Inherits from SpriteSheet for the explicit use of playing animations
class AnimatedSprite(SpriteSheet):

    def __init__(self, file_path: str, columns: int, rows: int, position: tuple[int, int],
                 colour_key: Colour = Colour(0, 0, 0), looping: bool = False) -> None:

        SpriteSheet.__init__(self, file_path, columns, rows, colour_key)

        self.__anim_frames = -1
        self.__can_loop = looping
        self.__position = position
        self.__hang_over = 0 # Number of frames for final frame to stick at screen

    # Macro for playing the next frame in an animation
    def animate_next_frame(self, surface):
        if self.__anim_frames >= 0:
            self.blit(surface=surface, sprite_id=self.__anim_frames, position=self.__position)
            self.__anim_frames += 1

            if self.__anim_frames >= self.sprite_count():
                if not self.__can_loop:
                    self.__anim_frames = -1
                elif self.__hang_over > 0:
                    self.__anim_frames = self.sprite_count() - 1
                    self.__hang_over -= 1
                else:
                    self.__anim_frames = 0

    # Macro for initializing an animation
    def start_animation(self, hang_over: int = 0):
        self.__hang_over = hang_over
        self.__anim_frames = 0

    # Set new location
    def update_position(self, new_position: tuple[int, int]):
        self.__position = new_position

    # Get current animation frame
    def get_frame(self):
        return self.__anim_frames
