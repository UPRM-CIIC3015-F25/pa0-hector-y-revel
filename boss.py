import pygame
import random

class EnemyBall:
    def __init__(self, x, y, screen_width):
        self.radius = 18
        self.x = x
        self.y = y
        self.speed_x = random.choice([-3, 3])
        self.speed_y = -3
        self.screen_width = screen_width

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce on left/right borders
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.speed_x *= -1
        elif self.x + self.radius >= self.screen_width:
            self.x = self.screen_width - self.radius
            self.speed_x *= -1

        # ✅ Bounce on top
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.speed_y *= -1

    def check_ball_collision(self, ball_rect, ball_speed):
        dx = self.x - ball_rect.centerx
        dy = self.y - ball_rect.centery
        dist = max((dx**2 + dy**2)**0.5, 0.1)
        combined_radius = self.radius + ball_rect.width / 2

        if dist < combined_radius:
            nx = dx / dist
            ny = dy / dist

            # Reflect velocities
            p_self = self.speed_x * nx + self.speed_y * ny
            p_ball = ball_speed[0] * nx + ball_speed[1] * ny

            self.speed_x += (p_ball - p_self) * nx
            self.speed_y += (p_ball - p_self) * ny

            ball_speed[0] += (p_self - p_ball) * nx
            ball_speed[1] += (p_self - p_ball) * ny

            # Separate them
            overlap = combined_radius - dist
            if overlap > 0:
                self.x += nx * overlap / 2
                self.y += ny * overlap / 2
                ball_rect.x -= int(nx * overlap / 2)
                ball_rect.y -= int(ny * overlap / 2)

    def collide_with_other(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        min_dist = self.radius + other.radius

        if dist < min_dist:
            # Normalize collision vector
            nx = dx / dist
            ny = dy / dist

            # Relative velocity
            dvx = self.speed_x - other.speed_x
            dvy = self.speed_y - other.speed_y
            rel_velocity = dvx * nx + dvy * ny

            if rel_velocity > 0:
                return  # They're moving apart already

            # Swap velocity along normal
            self.speed_x -= rel_velocity * nx
            self.speed_y -= rel_velocity * ny
            other.speed_x += rel_velocity * nx
            other.speed_y += rel_velocity * ny

            # Push them apart so they don't stick
            overlap = min_dist - dist
            self.x -= nx * overlap / 2
            self.y -= ny * overlap / 2
            other.x += nx * overlap / 2
            other.y += ny * overlap / 2

    def draw(self, surface):
        pygame.draw.circle(surface, (220, 50, 50), (int(self.x), int(self.y)), self.radius)


class Demon:
    def __init__(self, x, y, img_normal, img_hit, screen_width, screen_height):
        self.image_normal = img_normal
        self.image_hit = img_hit
        self.image = img_normal
        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = 3
        self.direction = 1
        self.shoot_timer = 0
        self.balls = []

        self.hit = False
        self.hit_timer = 0

        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, ball_rect, ball_speed):
        self.rect.x += self.speed * self.direction

        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction *= -1
        elif self.rect.right >= self.screen_width:
            self.rect.right = self.screen_width
            self.direction *= -1

        # Shoot
        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = 100
        else:
            self.shoot_timer -= 1

        # Update projectiles
        for proj in self.balls:
            proj.update()
            proj.check_ball_collision(ball_rect, ball_speed)

        # ✅ Handle projectile-to-projectile bouncing
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                self.balls[i].collide_with_other(self.balls[j])

        # Remove off-screen projectiles
        self.balls = [b for b in self.balls if 0 <= b.y <= self.screen_height]

        # Check collision with player ball
        if self.rect.colliderect(ball_rect):
            self.take_damage()

        # Sprite hit effect
        if self.hit:
            self.hit_timer -= 1
            if self.hit_timer <= 0:
                self.image = self.image_normal
                self.hit = False

    def shoot(self):
        bx = self.rect.centerx
        by = self.rect.top + 10
        self.balls.append(EnemyBall(bx, by, self.screen_width))

    def take_damage(self):
        self.image = self.image_hit
        self.hit = True
        self.hit_timer = 30

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        for ball in self.balls:
            ball.draw(surface)
