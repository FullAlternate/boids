from vectorExceptions import *
from precode import *
import random


class MovingObjects:
    def __init__(self, color):
        # Initialising objects with random attributes
        self.pos = Vector2D(random.randrange(20, 620), random.randrange(20, 460))
        self.velocity = Vector2D(random.randrange(1, 4), random.randrange(1, 4))
        self.color = color

    # Draws the object on the screen
    def draw(self, screen):

        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), 3)

    # Responsible for the discouragement of collision between certain objects
    # Takes two parameters, one that reduces how sensitive the objects are to collision
    # And another one that decides how close the objects can get before avoiding it
    # Returns a vector pointing away from the object marked for anti-collision
    def anti_collide(self, a_list, reduce, distance=15):
        vector = Vector2D(0, 0)

        for a in a_list:
            if a != self:

                if (a.pos.__sub__(self.pos)).__abs__() < distance:
                    vector = vector.__sub__(a.pos.__sub__(self.pos))

        try:
            vector = vector.__truediv__(reduce)

        except VectorZeroDivisionError:
            raise VectorZeroDivisionError("Can not divide vector by zero")
        except ScalarError:
            raise ScalarError("Right value must be castable to float")

        return vector

    # Encourages the objects to stay on screen
    # Returns a vector pointing away from the edge of the screen
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

        try:
            vector = vector.__truediv__(40)  # Prevents clunky animation by making the changes apply gradually

        except VectorZeroDivisionError:
            raise VectorZeroDivisionError("Can not divide vector by zero")
        except ScalarError:
            raise ScalarError("Right value must be castable to float")

        return vector

    # Limits the maximum speed objects can reach
    # Downscales the velocity if the objects surpass the speed limit
    def limit_speed(self, limit):

        if self.velocity.__abs__() > limit:
            try:
                self.velocity = (self.velocity.__truediv__(self.velocity.__abs__())).__mul__(limit)

            except VectorZeroDivisionError:
                raise VectorZeroDivisionError("Can not divide vector by zero")
            except ScalarError:
                raise ScalarError("Right value must be castable to float")


class Obstacle:
    def __init__(self):
        self.pos = Vector2D(0, 0)
        self.radius = 20
        self.color = (255, 165, 45)

    # Creates a new obstacle based on where the player clicks on the screen
    # Tracks the current position of the mouse and assigns this as the position of the new obstacle
    # Adds the new obstacle to the list parameter
    @staticmethod
    def create_obstacle(event, a_list):

        if event.type == pygame.MOUSEBUTTONDOWN:  # Tracks if a key is being pressed
            obs = Obstacle()

            x, y = pygame.mouse.get_pos()
            obs.pos = Vector2D(x, y)

            a_list.append(obs)

    # Draws the obstacles in the parameter list on the screen
    @staticmethod
    def draw(screen, a_list):

        for obstacle in a_list:
            pygame.draw.circle(screen, obstacle.color, (int(obstacle.pos.x), int(obstacle.pos.y)), obstacle.radius)


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

    # Responsible for the flocking behavior
    # Returns a vector pointing towards the average position of all other flock mates
    def flock(self, a_list):
        vector = Vector2D(0, 0)

        for b in a_list:
            if b != self:  # To exclude themselves when calculating the average position of the flock mates
                vector = vector.__add__(b.pos)

        if len(a_list) - 1 > 0:
            try:
                vector = vector.__truediv__(len(a_list) - 1)
                vector = vector.__sub__(self.pos)
                vector = vector.__truediv__(4000)  # Reduces intensity

            except VectorZeroDivisionError:
                raise VectorZeroDivisionError("Can not divide vector by zero")
            except ScalarError:
                raise ScalarError("Right value must be castable to float")

        return vector

    # Responsible for making boids steer towards the average heading of other flock mates
    # Returns a vector pointing in the general direction were all other boids are heading
    def heading(self, a_list):
        vector = Vector2D(0, 0)

        for b in a_list:
            if b != self:
                vector = vector.__add__(b.velocity)

        if len(a_list) - 1 > 0:
            try:
                vector = vector.__truediv__(len(a_list) - 1)
                vector = vector.__sub__(self.velocity)
                vector = vector.__truediv__(30)

            except VectorZeroDivisionError:
                raise VectorZeroDivisionError("Can not divide vector by zero")
            except ScalarError:
                raise ScalarError("Right value must be castable to float")

        return vector

    # Responsible for making boids flee from hoiks
    # Returns vectors pointing away from different hoiks
    def flee(self, element):

        try:
            vector = (element.pos.__sub__(self.pos)).__truediv__(3000)

        except VectorZeroDivisionError:
            raise VectorZeroDivisionError("Can not divide vector by zero")
        except ScalarError:
            raise ScalarError("Right value must be castable to float")

        return vector * -1


class Hoiks(MovingObjects):
    pass

    # Responsible for making hoiks chase boids
    # Returns vectors pointing towards different hoiks
    def chase(self, boid):

        try:
            vector = (boid.pos.__sub__(self.pos)).__truediv__(1000)

        except VectorZeroDivisionError:
            raise VectorZeroDivisionError("Can not divide vector by zero")
        except ScalarError:
            raise ScalarError("Right value must be castable to float")

        return vector


# Function for generating boids by clicking the spacebar button
# Appends the parameter list with the new boid object
def create_boid(event,a_list):

    if event.type == pygame.KEYDOWN:  # Tracks if a key is being pressed
        if event.key == pygame.K_SPACE:
            a_list.append(Boids((255, 255, 255)))


# Function for generating boids by clicking the h button
# Appends the parameter list with a new hoik object
def create_hoik(event, a_list):

    if event.type == pygame.KEYDOWN:  # Tracks if a key is being pressed
        if event.key == pygame.K_h:
            a_list.append(Hoiks((255, 0, 0)))


# Responsible for making all elements move according to the rules
# Adds all the returned rule vectors together and sets this to the object velocity
# Also draws the object on screen using the draw function
def move_elements(boids, hoiks, obstacles, screen):

    brule5 = Vector2D(0, 0)
    brule6 = Vector2D(0, 0)
    hrule3 = Vector2D(0, 0)

    for boid in boids:

        brule1 = boid.flock(boids)  # Makes boids flock together
        brule2 = boid.anti_collide(boids, 100)  # Discourages boids from colliding with each other
        brule3 = boid.heading(boids)  # Makes boids head in the same general direction
        brule4 = boid.bounding()  # Keeps boids on screen

        for hoik in hoiks:
            brule5 = boid.flee(hoik)  # Makes boids flee from hoiks
            brule6 = boid.anti_collide(hoiks, 300, 100)  # Discourages boids from colliding with hoiks

        brule7 = boid.anti_collide(obstacles, 250, 120)  # Discourages boids from colliding with circles

        boid.draw(screen)

        boid.velocity = boid.velocity.__add__(brule1.__add__(brule2.__add__(brule3.__add__(brule4.__add__
                                                                                           (brule5.__add__
                                                                                            (brule6.__add__
                                                                                             (brule7)))))))
        boid.limit_speed(5)

        boid.pos = boid.pos.__add__(boid.velocity)

    for hoik in hoiks:
        hrule1 = hoik.anti_collide(hoiks, 100)  # Prevents hoiks from colliding with each other
        hrule2 = hoik.bounding()  # Keeps hoiks on screen

        for boid in boids:
            hrule3 = hoik.chase(boid)  # Makes hoiks chase boids

        hrule4 = hoik.anti_collide(obstacles, 250, 120)  # Discourages hoiks from colliding with circles

        hoik.draw(screen)

        hoik.velocity = hoik.velocity.__add__(hrule1.__add__(hrule2.__add__(hrule3.__add__(hrule4))))
        hoik.limit_speed(4)

        hoik.pos = hoik.pos.__add__(hoik.velocity)


# The program function for running the simulation
def program():

    # Sets screen resolution
    the_screen = Screen((800, 600))

    circle_objects = Obstacle()

    # Initializing needed lists
    boids = []
    hoiks = []
    circles = []

    # Simulation loop
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            # All functions that rely on player input
            create_boid(event, boids)
            create_hoik(event, hoiks)
            circle_objects.create_obstacle(event, circles)

        the_screen.draw_screen()
        circle_objects.draw(the_screen.screen, circles)

        move_elements(boids, hoiks, circles, the_screen.screen)

        the_screen.lock_fps(60)  # Locks fps at 60
        pygame.display.update()  # Updates the screen


program()
