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
        self.speed = 100
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
        print("I got to this three!")
        for each in obstacles:
            if (
                x < 0
                or x >= GAME_WIDTH
                or y < 0
                or y >= GAME_HEIGHT
                or (x == each.position[0] and y == each.position[1])
            ):
                return True
        print("I got to this four!")
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
        self.image = pygame.transform.scale(
            pygame.image.load("bomb.png"), (SPACE_SIZE, SPACE_SIZE)
        )

    def randomize_position(self, bandaid, foods, snake):
        food_positions = []
        head = snake.body[0]
        for food in foods:
            food_positions.append(food.position)
        food_positions.append(bandaid.position)
        while True:
            self.position = [
                random.randrange(0, GAME_WIDTH - SPACE_SIZE, SPACE_SIZE),
                random.randrange(0, GAME_HEIGHT - SPACE_SIZE, SPACE_SIZE),
            ]
            if self.position in food_positions or self.position in snake.body:
                continue
            elif (
                self.position[0] == head[0] + 1
                or self.position[0] == head[0] - 1
                or self.position[1] == head[1] + 1
                or self.position[1] == head[1] - 1
            ):
                continue
            else:
                break


class Steak:
    def __init__(self):
        self.position = [
            random.randrange(0, GAME_WIDTH - SPACE_SIZE, SPACE_SIZE),
            random.randrange(0, GAME_WIDTH - SPACE_SIZE, SPACE_SIZE),
        ]
        self.image = pygame.transform.scale(
            pygame.image.load("steak.png"), (SPACE_SIZE, SPACE_SIZE)
        )
        self.expire = pygame.time.get_ticks() + 8000
        self.points = 5

    def has_expired(self, current_time):
        return current_time > self.expire


class Fruit:
    def __init__(self):
        self.position = [
            random.randrange(0, GAME_WIDTH - SPACE_SIZE, SPACE_SIZE),
            random.randrange(0, GAME_HEIGHT - SPACE_SIZE, SPACE_SIZE),
        ]
        self.image = pygame.transform.scale(
            pygame.image.load("apple.png"), (SPACE_SIZE, SPACE_SIZE)
        )
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
def choose_food():
    food = None
    choices = ["fruit", "steak"]
    weights = [0.85, 0.15]
    state = random.choices(choices, weights=weights)[0]

    if state is "fruit":
        food = Fruit()
    else:
        food = Steak()
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
    score = 0
    level = 1
    points = 0
    food_count = 0

    # Fonts for the score and level:
    font = pygame.font.Font(None, 36)

    # initializes first food and obstacle
    state = choose_food()
    foods.append(state)
    obs.append(Obstacle())
    if obs[0].position == foods[0].position:
        food_bandaid = foods[0]
        obs[0].randomize_position(food_bandaid, foods, snake)
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
        direction = astar(foods, obs, snake)

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
                food_bandaid = food
                foods.remove(food)
                for each in obs:
                    each.randomize_position(food_bandaid, foods, snake)
                score += food.points
                food_count += 1
                snake.grow()
                # snake.speed_up()
                temp = level
                level = int(math.ceil(score / 5))
                if temp < level:
                    obs.append(Obstacle())
                    obsCount += 1
                    for food in foods:
                        for each in obs:
                            if (
                                food in foods
                                and each.position[0] == food.position[0]
                                and each.position[1] == food.position[1]
                            ):
                                each.randomize_position(food_bandaid, foods, snake)
                if len(foods) == 0:
                    foods.append(choose_food())
                    for each in obs:
                        each.randomize_position(food_bandaid, foods, snake)
                break
        current_time = pygame.time.get_ticks()

        if current_time - last_interval >= 2000:
            if len(foods) <= 8:
                foods.append(choose_food())
                last_interval = current_time

        """COMMENT OUT TO REMOVE EXPIRATION"""
        foods = [food for food in foods if not food.has_expired(current_time)]

        while len(snake.body) > snake.growth:
            snake.body.pop()
        print("I got to this One!")
        # checks the snake head for collision
        if snake.check_collision(obs):
            points -= 100
            game_over(screen, score, level)
            break  # Exit the game loop when it's over
        print("I got to this Two!")
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

        food_text = font.render(f"Food: {food_count}", True, (0, 0, 0))
        screen.blit(food_text, (10, 70))

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


def astar(foods, obstacles, snake):
    head = snake.body[0]
    child_nodes = get_surrounding_nodes(snake, obstacles)
    child_choice = []
    lowest_heuristic = 1000000000000
    goal_state = [0, 0]
    for child in child_nodes:
        for food in foods:
            heuristic = heurisitc_func(child, food)
            if heuristic < lowest_heuristic:
                child_choice = child
                goal_state = food.position
                lowest_heuristic = heuristic
    print(f"Lowest Heuristic: {lowest_heuristic}\nThe Goal State: {goal_state}")
    print(f"Current Position: {head}. Go to {child_choice}")
    for child in child_nodes:
        print(f"Child Node: {child}")
    print(f"Amount of food on board: {len(foods)}\n")
    if child_choice != []:
        if head[0] != child_choice[0]:
            if head[0] < child_choice[0]:
                return "right"
            else:
                return "left"
        else:
            if head[1] < child_choice[1]:
                return "down"
            else:
                return "up"
    return snake.direction


def get_surrounding_nodes(snake, obstacles):
    frontier = []
    direction = snake.direction
    head = snake.body[0]
    if direction != "down":
        if head[1] != 0:
            frontier.append([head[0], head[1] - SPACE_SIZE])
    if direction != "up":
        if head[1] != 680:
            frontier.append([head[0], head[1] + SPACE_SIZE])
    if direction != "left":
        if head[0] != 680:
            frontier.append([head[0] + SPACE_SIZE, head[1]])
    if direction != "right":
        if head[0] != 0:
            frontier.append([head[0] - SPACE_SIZE, head[1]])
    
    new_frontier = []
    for node in frontier:
        removed = False
        for obs in obstacles:
            if node == obs.position:
                removed = True
                break
        for part in snake.body:
            if node == part:
                removed = True
                break
        if not removed:
            new_frontier.append(node)

    return new_frontier


def heurisitc_func(snake, food):
    """Just Manhattan Distance"""
    return abs(snake[0] - food.position[0]) + abs(snake[1] - food.position[1])
    """Weighs Food Points gives higher priority to higher point items"""
    # return abs(snake[0] - food.position[0]) + abs(snake[1] - food.position[1]) - food.points
    """Adds weight for expiration time"""
    # return (
    #     abs(snake[0] - food.position[0])
    #     + abs(snake[1] - food.position[1])
    #     - food.points
    #     + (food.expire - pygame.time.get_ticks())
    # )
    # return (-1 * food.points) + (food.expire - pygame.time.get_ticks())


if __name__ == "__main__":
    main()
