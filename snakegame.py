import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('Quicksand-Regular.otf', 25)

# reset after each game
# implement reward for agent
# game_iteration
# is_collision
# play_step

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# lightweight object to store coordinates
Point = namedtuple('Point', 'x, y')

# game constants
BLOCK_SIZE = 20
SPEED = 15

# rgb colours
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)


class SnakeGameAI:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

        # initialize display (screen)
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # initialize game state (initial positions of snake, food, direction)
        self.direction = Direction.RIGHT
        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head, \
                      Point(self.head.x-BLOCK_SIZE, self.head.y), 
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.height-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)

        # food should not appear on snake
        if self.food in self.snake:
            self._place_food()

    def _move(self, action):
        # [straight, right, left]
        clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clockwise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_direction = clockwise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_direction = clockwise[next_idx] # right turn
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_direction = clockwise[next_idx] # left turn

        self.direction = new_direction

        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        
        self.head = Point(x, y)

    def play_step(self, action):
        

        self.frame_iteration += 1
        # collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # move
        self._move(action)

        # update the snake head
        self.snake.insert(0, self.head)

        # check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            reward = -10
            game_over = True
            return reward, game_over, self.score
        
        # place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # return game over and score
        return reward, game_over, self.score

    def is_collision(self, point=None):
        if point is None:
            point = self.head
        # snake hits boundary
        if point.x > self.width - BLOCK_SIZE or point.x < 0 or point.y > self.height-BLOCK_SIZE or point.y < 0:
            return True
    
        # snake hits itself (check from 1st index to avoid head collision with itself)
        if point in self.snake[1:]:
            return True
        
        return False
    
    def _update_ui(self):
        self.display.fill(BLACK)
        
        # draw the snake
        for point in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(point.x+4, point.y+4, 12, 12))

        # draw the food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: {}".format(self.score), True, WHITE)
        self.display.blit(text, [0, 0])

        # update display
        pygame.display.flip()