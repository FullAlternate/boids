from precode2 import *


class MovingObjects:
    def __init__(self, pos, speed, color):
        self.pos = pos

        self.speed = speed
        self.color = color

    def draw(self, screen):
        pos_l = [(self.pos.x, self.pos.y), (self.pos.x + 10, self.pos.y - 15), (self.pos.x + 20, self.pos.y)]
        pygame.draw.polygon(screen, self.color, pos_l)

    def move(self):
        self.pos.x += self.speed.x
        self.pos.y += self.speed.y


class Screen:
    def __init__(self, screen_res):
        self.screen = pygame.display.set_mode(screen_res)
        self.clock = pygame.time.Clock()

    def draw_screen(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.screen.get_width(), self.screen.get_height()))

    def lock_fps(self, fps):
        self.clock.tick(fps)


def boids():

    theScreen = Screen((640, 480))
    boid = MovingObjects(Vector2D(400, 400), Vector2D(-1, -0.1), (255, 255, 255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        theScreen.draw_screen()
        boid.draw(theScreen.screen)
        boid.move()

        theScreen.lock_fps(60)
        pygame.display.update()


boids()
