from collections import namedtuple
from random import randint
import pygame


Colour = namedtuple('Colour', ['red', 'green', 'blue'])
BACKGROUND_COLOUR = Colour(red=50, green=150, blue=150)
SNAKE_COLOUR = Colour(red=230, green=215, blue=125)
FOOD_COLOUR = Colour(red=255, green=150, blue=75)
TEXT_COLOUR = Colour(red=75, green=200, blue=25)
END_TEXT_COLOUR = Colour(red=175, green=25, blue=25)
ENDSCREEN_COLOUR = Colour(red=5, green=5, blue=5)

SNAKE_SEGMENT_RADIUS = 10
SEGMENT = SNAKE_SEGMENT_RADIUS * 2
FOOD_RADIUS = SNAKE_SEGMENT_RADIUS
GAME_SPEED = 10

HEIGHT = SEGMENT * 32
WIDTH = HEIGHT
STATUS_BAR_HEIGHT = 50

pygame.init()
pygame.display.set_caption('Snake game')
clock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])


class Snake:
    positions = []

    def __init__(self, surface, colour, position, radius):
        self.surface = surface
        self.colour = colour
        self.position = position
        self.radius = radius
        self.extend(position)

    def extend(self, position):
        self.positions.append(position)

    def move(self, direction):
        if self.positions:
            x, y = self.positions[0]
            if direction == 'up':
                new_position = [x, y - SEGMENT]
            elif direction == 'down':
                new_position = [x, y + SEGMENT]
            elif direction == 'left':
                new_position = [x - SEGMENT, y]
            elif direction == 'right':
                new_position = [x + SEGMENT, y]

            self.positions.insert(0, new_position)
            self.positions.pop(-1)
            self.draw()

    def draw(self):
        screen.fill(BACKGROUND_COLOUR)
        for position in self.positions:
            if position[0] < SNAKE_SEGMENT_RADIUS:
                position[0] = HEIGHT - SNAKE_SEGMENT_RADIUS
            elif position[0] > HEIGHT - SNAKE_SEGMENT_RADIUS:
                position[0] = SNAKE_SEGMENT_RADIUS
            if position[1] < SNAKE_SEGMENT_RADIUS:
                position[1] = WIDTH - SNAKE_SEGMENT_RADIUS
            elif position[1] > WIDTH - SNAKE_SEGMENT_RADIUS:
                position[1] = SNAKE_SEGMENT_RADIUS

            pygame.draw.circle(
                self.surface,
                self.colour,
                position,
                self.radius
                )


def place_food(snake_positions):
    while True:
        segments_num = HEIGHT / SEGMENT
        x_coord = randint(0, segments_num-1)*SEGMENT + FOOD_RADIUS
        y_coord = randint(0, segments_num-1)*SEGMENT + FOOD_RADIUS
        food_position = [x_coord, y_coord]
        if food_position not in snake_positions:
            return food_position


def check_snake_collision(positions):
    for position in positions[1:]:
        if position == positions[0]:
            return True


def check_feeding(food_position, snake_positions):
    if snake_positions[0] == food_position:
        return True


snake = Snake(
    screen,
    SNAKE_COLOUR,
    [(SEGMENT/2)*5, (SEGMENT/2)*5],
    SNAKE_SEGMENT_RADIUS
    )
new_position = snake.position[0], snake.position[1] + SEGMENT
snake.extend(new_position)
new_position = snake.position[0], snake.position[1] + 2*SEGMENT
snake.extend(new_position)


screen.fill(BACKGROUND_COLOUR)
snake.draw()
pygame.display.update()


def main():
    score = 0
    motion = 'right'
    food_position = place_food(snake.positions)
    while True:
        if not check_snake_collision(snake.positions):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                if motion != 'up':
                    motion = 'down'
            elif keys[pygame.K_UP]:
                if motion != 'down':
                    motion = 'up'
            elif keys[pygame.K_LEFT]:
                if motion != 'right':
                    motion = 'left'
            elif keys[pygame.K_RIGHT]:
                if motion != 'left':
                    motion = 'right'

            snake.move(motion)
            pygame.draw.circle(screen, FOOD_COLOUR, food_position, FOOD_RADIUS)
            if check_feeding(food_position, snake.positions):
                score += 1
                snake.extend(snake.positions[1])
                food_position = place_food(snake.positions)

            font = pygame.font.Font(None, 28)
            text = font.render(f"Score: {score}", True, TEXT_COLOUR)
            screen.blit(text, (10, 10))

            pygame.display.update()
            clock.tick(GAME_SPEED)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            screen.fill(ENDSCREEN_COLOUR)
            font = pygame.font.Font(None, 76)
            text = font.render(
                f'You scored {score} points',
                True,
                END_TEXT_COLOUR
                )
            screen.blit(text, [60, HEIGHT//2])
            pygame.display.update()
            clock.tick(GAME_SPEED)


main()
