# Packages required
import heapq
import math
import itertools
import copy
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPACE_SIZE = 20
  
class Problem(object):
    """The abstract class for a formal problem. A new domain subclasses this,
    overriding `actions` and `results`, and perhaps other methods.
    The default heuristic is 0 and the default action cost is 1 for all states.
    When yiou create an instance of a subclass, specify `initial`, and `goal` states 
    (or give an `is_goal` method) and perhaps other keyword args for the subclass."""

    def __init__(self, initial=None, goal=None, **kwds): 
        self.__dict__.update(initial=initial, goal=goal, **kwds) 
        
    def actions(self, state):        raise NotImplementedError
    def result(self, state, action): raise NotImplementedError
    def is_goal(self, state):        return state == self.goal
    def action_cost(self, s, a, s1): return 1
    def h(self, node):               return 0
    
    def __str__(self):
        return '{}({!r}, {!r})'.format(
            type(self).__name__, self.initial, self.goal)
    

class Node:
    "A Node in a search tree."
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.__dict__.update(state=state, parent=parent, action=action, path_cost=path_cost)

    def __repr__(self): return '<{}>'.format(self.state)
    def __len__(self): return 0 if self.parent is None else (1 + len(self.parent))
    def __lt__(self, other): return self.path_cost < other.path_cost
    
    
failure = Node('failure', path_cost=math.inf) # Indicates an algorithm couldn't find a solution.
cutoff  = Node('cutoff',  path_cost=math.inf) # Indicates iterative deepening search was cut off.

def expand(problem, node):
    "Expand a node, generating the children nodes."
    s = node.state
    problem.expanded += 1
    for action in problem.actions(s):
        s1 = problem.result(s, action)
        # problem.repr(s1) # DEBUG
        cost = node.path_cost + problem.action_cost(s, action, s1)
        yield Node(s1, node, action, cost)
        

def path_actions(node):
    "The sequence of actions to get to this node."
    if node.parent is None:
        return []  
    return path_actions(node.parent) + [node.action]


def path_states(node):
    "The sequence of states to get to this node."
    if node in (cutoff, failure, None): 
        return []
    return path_states(node.parent) + [node.state]

class PriorityQueue:
    """A queue in which the item with minimum f(item) is always popped first."""

    def __init__(self, items=(), key=lambda x: x): 
        self.key = key
        self.items = [] # a heap of (score, item) pairs
        for item in items:
            self.add(item)
         
    def add(self, item):
        """Add item to the queuez."""
        pair = (self.key(item), item)
        heapq.heappush(self.items, pair)

    def pop(self):
        """Pop and return the item with min f(item) value."""
        return heapq.heappop(self.items)[1]
    
    def top(self): return self.items[0][1]

    def __len__(self): return len(self.items)

def is_cycle(node, k=30):
    "Does this node form a cycle of length k or less?"
    def find_cycle(ancestor, k):
        return (ancestor is not None and k > 0 and
                (ancestor.state == node.state or find_cycle(ancestor.parent, k - 1)))
    return find_cycle(node.parent, k)

def best_first_tree_search(problem, f):
    frontier = PriorityQueue([Node(problem.initial)], key=f)
    # print(frontier.__len__()) # DEBUG
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            if not is_cycle(child):
                frontier.add(child)
            
    return failure

def g(n): return n.path_cost

def astar_tree_search(problem, h=None):
    """Search nodes with minimum f(n) = g(n) + h(n)."""
    h = problem.h
    return best_first_tree_search(problem, f=lambda n: g(n) + h(n))

class SnakeProblem(Problem):

    def __init__(self, foods, obs, snake, heuristic, goal=None, initial=None):
        #stuff

        self.foods = foods
        self.obs = obs
        self.snake = snake
        self.num_food = self.num_foods(self.foods)

        # self.rand = False

        if len(foods) != 0:
            food_list = []
            for food in foods:
                food_list.append([food.points, [food.position[0], food.position[1]]])

        obs_list = []
        for obs in self.obs:
            obs_list.append(obs.position)

        self.initial = (food_list, obs_list, self.snake.body)

        lowest_heuristic = 1000000
        self.goal_food = [0,0]
        if len(food_list) == 0:
            self.goal_food[0] = 1
            self.goal_food[0] = 1
        else:
            for food in food_list:
                heuristic = self.heuristic_one(self.snake.body[0], food[1])
                heuristic = heuristic - food[0]
                if heuristic < lowest_heuristic:
                    self.goal_food = food[1]
                    lowest_heuristic = heuristic

        self.goal = tuple(self.goal_food)
        self.expanded = 0

        # print(f"INIT SNAKE: {self.snake.body[0]}")
        # print(f"INIT GOAL: {self.goal}")
        # for part in snake.body:
        #     print(f"PART: {part}")

        Problem.__init__(self, initial=self.initial, goal=self.goal)


    def actions(self, state): 
        
        actions = []
        snake = copy.deepcopy(state[2])
        head = [0,0]
        head[0] = snake[0][0]
        head[1] = snake[0][1]

        # print(f"STATE HEAD: {state[2].body[0][0]}, {state[2].body[0][1]}")
        # print(f"HEAD: {head[0]}, {head[1]}")

        if head[1] != 0:
                actions.append((head[0], head[1] - SPACE_SIZE))

        if head[1] != 680:
                actions.append((head[0], head[1] + SPACE_SIZE))

        if head[0] != 680:
                actions.append((head[0] + SPACE_SIZE, head[1]))

        if head[0] != 0:
                actions.append((head[0] - SPACE_SIZE, head[1]))


        if len(snake) > 1 and (snake[1][1] < head[1]):
                actions.remove((head[0], head[1] - SPACE_SIZE))

        if len(snake) > 1 and (snake[1][1] > head[1]):
                actions.remove((head[0], head[1] + SPACE_SIZE))

        if len(snake) > 1 and (snake[1][0] > head[0]):
                actions.remove((head[0] + SPACE_SIZE, head[1]))

        if len(snake) > 1 and (snake[1][0] < head[0]):
                actions.remove((head[0] - SPACE_SIZE, head[1]))

        # i = 0
        new_actions = []
        for node in actions:
            removed = False
            for obs in state[1]:
                if node[0] == obs[0] and node[1] == obs[1]:
                    # print("Obstacle node removed")
                    removed = True
                    break
            for part in snake:
                # print(f"PART {i}: {part}")
                # i += 1
                if node[0] == part[0] and node[1] == part[1]:
                    removed = True
                    break
            if not removed:
                new_actions.append(node)

        #DEBUG
        # print("SET:")
        # for a in actions:
        #     print(a)

        return new_actions
    

    def result(self, state, action):
        snake = copy.deepcopy(state[2])

        snake.insert(0, copy.deepcopy(action))

        if(len(snake) > 1):
            snake.pop()

        new_state = (copy.deepcopy(state[0]), copy.deepcopy(state[1]), snake)

        # print(f"ACTION: {action}")
        # print(f"NEW HEAD: {snake[0]}")
        # for part in snake.body:
        #     print(f"PART: {part}")
        # print(new_state)
        # print(state)
       
        return new_state
    
    def is_goal(self, state):
        snake = state[2]
        #DEBUG
        # print(f"SNAKE: {snake[0]}")
        # print(f"GOAL {self.goal}")
        return (snake[0] == self.goal)

    def num_foods(self, foods):
        num_food = 0
        for food in foods:
            num_food = num_food + 1
        return num_food
    
    def h(self, node): 
        snake = node.state[2]
        dist = self.heuristic_four(snake[0], self.goal)
        # print(f"DIST: {dist}")
        return dist

    def heuristic_one(self, snake, food):
        return (abs(snake[0] - food[0]) + abs(snake[1] - food[1]))/20
    
    def heuristic_two(self, snake, food):
        dist = (abs(snake[0] - food[0]))
        dist = dist + (abs(snake[1] - food[1])) * 0.95
        return dist     
    
    def heuristic_three(self, snake, food):
         return math.sqrt(abs(snake[0] - food[0])**2 + abs(snake[1] - food[1])**2)
    
    def heuristic_four(self, snake, food):
         dist = self.heuristic_one(snake, food)
         dist += self.heuristic_three(snake, food)
         return dist
    
