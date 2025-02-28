from constants import *

# Player class
class Player:
    def __init__(self):
        self.position = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = pygame.math.Vector2(0, 0)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.velocity.y -= 0.1
        if keys[pygame.K_s]:
            self.velocity.y += 0.1
        if keys[pygame.K_a]:
            self.velocity.x -= 0.1
        if keys[pygame.K_d]:
            self.velocity.x += 0.1

        self.position += self.velocity
        self.velocity *= 0.9

