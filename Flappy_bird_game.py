import pygame
import random
import sys

# Constants
WIDTH = 400
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
GRAVITY = 0.25
FLAP_SPEED = -5

class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.vel_y = 0
        self.img = pygame.image.load("bird.png").convert()
        self.img.set_colorkey(WHITE)
        self.rect = self.img.get_rect(center=(self.x, self.y))

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y
        self.rect.centery = self.y

    def flap(self):
        self.vel_y = FLAP_SPEED

    def draw(self, screen):
        screen.blit(self.img, self.rect)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.y = 0
        self.gap = 150
        self.height = random.randint(50, HEIGHT - self.gap - 50)
        self.img_top = pygame.image.load("pipe.png").convert()
        self.img_bottom = pygame.transform.flip(self.img_top, False, True)
        self.rect_top = self.img_top.get_rect(topleft=(self.x, self.y))
        self.rect_bottom = self.img_bottom.get_rect(topleft=(self.x, self.height + self.gap))

    def update(self):
        self.x -= 3
        self.rect_top.left = self.x
        self.rect_bottom.left = self.x

    def draw(self, screen):
        screen.blit(self.img_top, self.rect_top)
        screen.blit(self.img_bottom, self.rect_bottom)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    bird = Bird()
    pipes = []
    game_over = False
    score = 0
    font = pygame.font.Font(None, 36)

    def create_pipe():
        x = WIDTH + 50
        pipe = Pipe(x)
        pipes.append(pipe)

    def check_collision(bird, pipes):
        if bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT:
            return True
        for pipe in pipes:
            if bird.rect.colliderect(pipe.rect_top) or bird.rect.colliderect(pipe.rect_bottom):
                return True
        return False

    def update_score(score):
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    create_pipe_event = pygame.USEREVENT
    pygame.time.set_timer(create_pipe_event, 1500)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
            if event.type == create_pipe_event:
                create_pipe()

        screen.fill(WHITE)

        bird.update()
        bird.draw(screen)

        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)
            if pipe.x + pipe.img_top.get_width() < 0:
                pipes.remove(pipe)
                score += 1

        game_over = check_collision(bird, pipes)
        update_score(score)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
