# key features of the Python Snake game

# Player direction control using arrow keys (up, down, left, and right).

# Colorful food items are placed randomly on the game grid.

# The snake's objective is to eat these food items to grow and score points.

# Player's current score is displayed on the screen.

# Scoring increases by one point for each food item consumed.

# The game may feature a level system that increases in difficulty.

# Levels may increase based on the player's score (e.g., every 5 points).

# The snake's movement speed increases as the player's score rises.

# Game ends if the snake hits the game window's boundaries.

# Game ends if the snake collides with its own body.

# Upon collision, a "Game Over" screen is displayed with player's final score and level.

import sys
import pygame
import random
import math
from aima_python_functs import *

# Constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPACE_SIZE = 20
SNAKE_COLOR = (0, 255, 0)
BACKGROUND_COLOR = (255, 255, 255)

class Snake:
    def __init__(self):
        self.body = [[0, 0]]
        self.direction = "right"
        self.speed = 50
        self.growth = 1

    def change_direction(self, new_direction):
        if new_direction == "left" and self.direction != "right":
            self.direction = new_direction
        if new_direction == "right" and self.direction != "left":
            self.direction = new_direction
        if new_direction == "up" and self.direction != "down":
            self.direction = new_direction
        if new_direction == "down" and self.direction != "up":
            self.direction = new_direction

    def move(self):
        x, y = self.body[0]
        if self.direction == "up":
            y -= SPACE_SIZE
        if self.direction == "down":
            y += SPACE_SIZE
        if self.direction == "left":
            x -= SPACE_SIZE
        if self.direction == "right":
            x += SPACE_SIZE
        self.body.insert(0, [x, y])

    def check_collision(self, obstacles):
        x, y = self.body[0]
        for each in obstacles:
            if (
                x < 0
                or x >= GAME_WIDTH
                or y < 0
                or y >= GAME_HEIGHT
                or (x == each.position[0] and y == each.position[1])
            ):
                return True
        for part in self.body[1:]:
            if x == part[0] and y == part[1]:
                return True
        return False

    def grow(self):
        self.growth += 1

    def speed_up(self):
        self.speed += 1


class Obstacle:
    def __init__(self):
        self.position = [
            random.randrange(0, GAME_WIDTH - SPACE_SIZE, SPACE_SIZE),
            random.randrange(0, GAME_WIDTH - SPACE_SIZE, SPACE_SIZE),
        ]
        self.points = -100
        self.image = pygame.transform.scale(pygame.image.load("bomb.png"), (SPACE_SIZE, SPACE_SIZE))

    def randomize_position(self, foods, body):
        while True:
            conflict = False
            self.position = [
            random.randrange(0, GAME_WIDTH - SPACE_SIZE, SPACE_SIZE),
            random.randrange(0, GAME_HEIGHT - SPACE_SIZE, SPACE_SIZE),
        ]
            for food in foods:
                if self.position == food.position:
                    conflict = True
            for part in body:
                if self.position == part:
                    conflict = True
            if conflict:
                continue
            else:
                break
            


class Steak:
    def __init__(self, obs, body):
        # self.position = [
        #     random.randrange(0, GAME_WIDTH - SPACE_SIZE, SPACE_SIZE),
        #     random.randrange(0, GAME_WIDTH - SPACE_SIZE, SPACE_SIZE),
        # ]
        
        while True:
            conflict = False
            self.position = [
            random.randrange(0, GAME_WIDTH - SPACE_SIZE, SPACE_SIZE),
            random.randrange(0, GAME_HEIGHT - SPACE_SIZE, SPACE_SIZE),
        ]
            for ob in obs:
                if self.position == ob.position:
                    conflict = True
            for part in body:
                if self.position == part:
                    conflict = True
            if conflict:
                continue
            else:
                break

        self.image = pygame.transform.scale(pygame.image.load("steak.png"), (SPACE_SIZE, SPACE_SIZE))
        self.expire = pygame.time.get_ticks() + 8000
        self.points = 5
        self.cost = 1 #NOTE: I added costs here
        
    def has_expired(self, current_time):
        return current_time > self.expire


class Fruit:
    def __init__(self, obs, body):
        # self.position = [
        #     random.randrange(0, GAME_WIDTH - SPACE_SIZE, SPACE_SIZE),
        #     random.randrange(0, GAME_HEIGHT - SPACE_SIZE, SPACE_SIZE),
        # ]
        while True:
            conflict = False
            self.position = [
            random.randrange(0, GAME_WIDTH - SPACE_SIZE, SPACE_SIZE),
            random.randrange(0, GAME_HEIGHT - SPACE_SIZE, SPACE_SIZE),
        ]
            for ob in obs:
                if self.position == ob.position:
                    conflict = True
            for part in body:
                if self.position == part:
                    conflict = True
            if conflict:
                continue
            else:
                break

        self.image = pygame.transform.scale(pygame.image.load("apple.png"), (SPACE_SIZE, SPACE_SIZE))
        self.expire = pygame.time.get_ticks() + 12000
        self.points = 1

    def has_expired(self, current_time):
        return current_time > self.expire

def game_over(screen, score, level):
    font = pygame.font.Font(None, 72)
    text = font.render(f"Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 20))
    screen.blit(score_text, score_rect)

    level_text = font.render(f"Level: {level}", True, (0, 0, 0))
    level_rect = level_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 60))
    screen.blit(level_text, level_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# randomly spawns food
def choose_food(obs, body):
    food = None
    choices = ["fruit", "steak"]
    weights = [0.85, 0.15]
    state = random.choices(choices, weights=weights)[0]
    
    if state is "fruit":
        food = Fruit(obs, body)
    else:
        food = Steak(obs, body)
    return food

def main():
    last_interval = pygame.time.get_ticks()
    
    pygame.init()
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    last_food_time = pygame.time.get_ticks()
    snake = Snake()
    foods = []
    obs = []
    obsCount = 0
    obs.append(Obstacle())
    score = 0
    level = 1
    points = 0

    # Fonts for the score and level:
    font = pygame.font.Font(None, 36)
    
    # initializes first food
    state = choose_food(obs, snake.body)
    foods.append(state)
    while True:
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         quit()
        #     # we are going to change this from events to the AI's choice!!!!!
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_UP:
        #             snake.change_direction("up")
        #         if event.key == pygame.K_DOWN:
        #             snake.change_direction("down")
        #         if event.key == pygame.K_LEFT:
        #             snake.change_direction("left")
        #         if event.key == pygame.K_RIGHT:
        #             snake.change_direction("right")
        
        #NOTE: Make into function
        Problem = SnakeProblem(foods, obs, snake, heurisitc_one)
        # for s in path_states(astar_tree_search(Problem)):
        #     print(s)
        # for a in path_actions(astar_tree_search(Problem)):
        #     print(a)

        a = path_actions(astar_tree_search(Problem))[0]
        head = snake.body[0]
        # print(f"HEAD: {head}")
        print(f"MOVE: {a}")

        if head[0] != a[0]:
            if head[0] < a[0]:
                direction = "right"
            else:
                direction = "left"
        else:
            if head[1] < a[1]:
                direction = "down"
            else:
                direction = "up"
        
        if direction == "up":
            snake.change_direction("up")
        elif direction == "down":
            snake.change_direction("down")
        elif direction == "left":
            snake.change_direction("left")
        elif direction == "right":
            snake.change_direction("right")
        
        # moves the snake based on input
        snake.move()

        # checks if a food was picked up
        for food in foods:
            if snake.body[0] == food.position:
                for each in obs:
                    each.randomize_position(foods, snake.body)
                # obs[-1].randomize_position(foods)
                score += food.points
                # if len(snake.body) < 40:
                snake.grow()
                #snake.speed_up()
                temp = level
                level = int(math.ceil(score / 5))
                if temp < level:
                    obs.append(Obstacle())
                    obsCount += 1
                foods.remove(food)
                if len(foods) == 0:
                    foods.append(choose_food(obs, snake.body))
                break
        current_time = pygame.time.get_ticks()
        
        if current_time - last_interval >= 2000:
            if len(foods) <= 8:
                foods.append(choose_food(obs, snake.body))
                last_interval = current_time
                
        """COMMENT OUT TO REMOVE EXPIRATION"""
        #foods = [food for food in foods if not food.has_expired(current_time)]

        while len(snake.body) > snake.growth:
            snake.body.pop()

        # checks the snake head for collision
        if snake.check_collision(obs):
            points -= 100
            game_over(screen, score, level)
            break  # Exit the game loop when it's over

        screen.fill(BACKGROUND_COLOR)
        for part in snake.body:
            pygame.draw.rect(
                screen, SNAKE_COLOR, (part[0], part[1], SPACE_SIZE, SPACE_SIZE)
            )

        # Display the score and level:
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        level_text = font.render(f"Level: {level}", True, (0, 0, 0))
        screen.blit(level_text, (10, 40))
        
        # spawn all foods
        for food in foods:
            screen.blit(food.image, (food.position[0], food.position[1]))
            # print(food.position[0], food.position[1])
        
        # print(snake.body[0])
        
        # spawn all obstacles
        for each in obs:
            screen.blit(each.image, (each.position[0], each.position[1]))
        # update the display
        pygame.display.update()
        clock.tick(snake.speed)
        
def heurisitc_one(snake, food):
    return (abs(snake[0] - food[0]) + abs(snake[1] - food[1]))/20

if __name__ == "__main__":
    main()