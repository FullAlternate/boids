from precode import *
import random


class MovingObjects:
    def __init__(self, color):
        self.pos = Vector2D(random.randrange(20, 620), random.randrange(20, 460))
        self.velocity = Vector2D(2, 2)
        self.color = color

    def draw(self, screen):

        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), 3)

    def flock(self, a_list):
        vector = Vector2D(0, 0)

        for b in a_list:
            if b != self:
                vector = vector.__add__(b.pos)

        if len(a_list) - 1 > 0:
            vector = vector.__truediv__(len(a_list) - 1)
            vector = vector.__sub__(self.pos)
            vector = vector.__truediv__(4000)
        return vector

    def anti_collide(self, a_list, reduce, distance = 15):
        vector = Vector2D(0, 0)

        for b in a_list:
            if b != self:

                if (b.pos.__sub__(self.pos)).__abs__() < distance:
                    vector = vector.__sub__(b.pos.__sub__(self.pos))

        vector = vector.__truediv__(reduce)

        return vector

    def heading(self, a_list):
        vector = Vector2D(0, 0)

        for b in a_list:
            if b != self:
                vector = vector.__add__(b.velocity)

        if len(a_list) - 1 > 0:
            vector = vector.__truediv__(len(a_list) - 1)
            vector = vector.__sub__(self.velocity)
            vector = vector.__truediv__(30)
        return vector

    def bounding(self):
        x_min = 50
        x_max = 750
        y_min = 50
        y_max = 550
        vector = Vector2D(0, 0)

        if self.pos.x < x_min:
            vector.x = 10

        elif self.pos.x > x_max:
            vector.x = -10

        if self.pos.y < y_min:
            vector.y = 10

        elif self.pos.y > y_max:
            vector.y = -10

        vector = vector.__truediv__(40)
        return vector

    def limit_speed(self, limit):

        if self.velocity.__abs__() > limit:
            self.velocity = (self.velocity.__truediv__(self.velocity.__abs__())).__mul__(limit)

class obstacle:
    def __init__(self):
        self.pos = Vector2D(0, 0)
        self.radius = 15
        self.color = (255, 165, 45)

    def draw(self, screen, event):
        x, y = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:  # Tracks if a key is being pressed
            if event.key == pygame.mouse.get_pressed():
                self.pos = Vector2D(x, y)
                pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)


class Screen:
    def __init__(self, screen_res):
        self.screen = pygame.display.set_mode(screen_res)
        self.clock = pygame.time.Clock()

    def draw_screen(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.screen.get_width(), self.screen.get_height()))

    def lock_fps(self, fps):
        self.clock.tick(fps)

class Boids(MovingObjects):
    pass

    def flee(self, element):

        vector = (element.pos.__sub__(self.pos)).__truediv__(3000)
        return vector * -1


class Hoiks(MovingObjects):
    pass

    def chase(self, boid):

        vector = (boid.pos.__sub__(self.pos)).__truediv__(1000)
        return vector



def create_boid(event,list):

    if event.type == pygame.KEYDOWN:  # Tracks if a key is being pressed
        if event.key == pygame.K_SPACE:
            list.append(Boids((255, 255, 255)))


def create_hoik(event, list):

    if event.type == pygame.KEYDOWN:  # Tracks if a key is being pressed
        if event.key == pygame.K_h:
            list.append(Hoiks((255, 0, 0)))


def move_elements(boids, hoiks, screen):

    brule5 = Vector2D(0, 0)
    brule6 = Vector2D(0, 0)
    hrule3 = Vector2D(0, 0)

    for boid in boids:

        brule1 = boid.flock(boids)
        brule2 = boid.anti_collide(boids, 100)
        brule3 = boid.heading(boids)
        brule4 = boid.bounding()

        for hoik in hoiks:
            brule5 = boid.flee(hoik)
            brule6 = boid.anti_collide(hoiks, 300, 100)

        boid.draw(screen)

        boid.velocity = boid.velocity.__add__(brule1.__add__(brule2.__add__(brule3.__add__(brule4.__add__(brule5.__add__(brule6))))))
        boid.limit_speed(5)

        boid.pos = boid.pos.__add__(boid.velocity)

    for hoik in hoiks:
        hrule1 = hoik.anti_collide(hoiks, 100)
        hrule2 = hoik.bounding()

        for boid in boids:
            hrule3 = hoik.chase(boid)

        hoik.draw(screen)

        hoik.velocity = hoik.velocity.__add__(hrule1.__add__(hrule2.__add__(hrule3)))
        hoik.limit_speed(4)

        hoik.pos = hoik.pos.__add__(hoik.velocity)


def program():

    theScreen = Screen((800, 600))

    boids = []
    hoiks = []


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            create_boid(event, boids)
            create_hoik(event, hoiks)

        theScreen.draw_screen()
        move_elements(boids, hoiks, theScreen.screen)


        theScreen.lock_fps(60)
        pygame.display.update()


program()
