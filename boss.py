import pygame

sprites = ['cacodemon.png', 'cacodemon2.png']

class Demon:
    def __init__(self, x, y, image_path, speed=2, move=100):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.start_x = x
        self.move = move
        self.direction = 1

    def update(self):
        # Move the enemy
        self.rect.x += self.speed * self.direction

        # Reverse direction at patrol edges
        if abs(self.rect.x - self.start_x) >= self.move:
            self.direction *= -1

    def draw(self, surface):
        surface.blit(self.image, self.rect)

