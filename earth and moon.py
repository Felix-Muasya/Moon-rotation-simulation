import pygame
import math

pygame.init()

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moon Rotation Simulation")

WHITE = (255, 255, 255)
BLUE = (100, 149, 237)

FONT = pygame.font.SysFont("comicsans", 16)


class Satellite:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 100/AU
    TIMESTEP = 3600 * 24

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.earth = False
        self.distance_to_earth = 0

        # velocity of the moon
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):

        # placing the earth in the middle of the window
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.earth:
            distance_text = FONT.render(f"{round(self.distance_to_earth / 1000, 1)} km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.earth:
            self.distance_to_earth = distance

        force = self.G * self.mass * other.mass/distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, satellites):
        total_fx = total_fy = 0
        for satellite in satellites:
            if self == satellite:
                continue

            fx, fy = self.attraction(satellite)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()
# inputing the data fro the earth and moon
    earth = Satellite(0, 0, 50, BLUE, 5.9742 * 10 ** 24)
    earth.earth = True

    moon = Satellite(1.524 * Satellite.AU, 0, 16, WHITE, 7.347 * 10 ** 22)
    moon.y_vel = 1.022*1000

    satellites = [earth, moon]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for satellite in satellites:
            satellite.update_position(satellites)
            satellite.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
# TODO find out why x isn't being updated