from utils import *
from search import *
import math


# Environmental Boundries and Information:
# ================================================================================


# ACTIONS List
# Each change in poistion 
UP       = (-1,0)
DOWN     = (1,0)
LEFT     = (0,-1)
RIGHT    = (0,1)
ACTIONS =   [UP, DOWN, LEFT, RIGHT]


class SnakeProblem(Problem):

    def __init__(self, initial):
        #Inherits class Problem.
        super().__init__(initial)
        self.total_cost = 0

    # Method to determine the allowed actions at a current state
    # Should this be all of them because it can kill itself?
    # Need to remove the oposite direction of travel
    def actions(self, state):
        allowedActions = ACTIONS.copy()

         # Conversion Code from Tuple to Lists 
        # SnakeProblem((tuple(snakeList),tuple(foodList),tuple(obsList))
        newState = list(state)

        snake = list(newState[0])
        obsList = list(newState[2])

        headY,headX = snake[0]

        # Code to prevent Out of Bounds
        #===========================================================================


        # If the head is on the left edge of the 35/35 grid, remove up action
        if headX == 0:
            allowedActions.remove(LEFT)
        # If the head is on the right edge of the 35/35 grid, remove down action
        if headX == 34:
            allowedActions.remove(RIGHT)
        # If the vacuum is on the top edge of 35/35 grid, remove up action
        if headY == 0:
            allowedActions.remove(UP)
        # If the vacuum is on the top edge of 35/35 grid, remove up action
        if headY == 34:
            allowedActions.remove(DOWN)

        #===========================================================================


        # Code to prevent Hitting a Obs or the snakes body
        #===========================================================================

        # This is suppose to remove the results that make the agent move into itself or a obstical but it does not
        for action in allowedActions:
            head = snake[0]
            resultX = head[0]+action[0]
            resultY = head[1]+action[1]
            print(f"Results:{(resultX,resultY)}")
            if((resultX,resultY) in snake or ((resultX,resultY) in obsList)):
                allowedActions.remove(action)
        
        #===========================================================================



        # If we need to restrict actions then this section needs to check all of the possible 
        return allowedActions


    # Define the succesor result function
    # This function will take in the current state and then update it to the new state
    def result(self, state, action):
    
        # Conversion Code from Tuple to Lists 
        # SnakeProblem((tuple(snakeList),tuple(foodList),tuple(obsList)))
        newState = list(state)

        snake = list(newState[0])
        foodList = list(newState[1])
        obsList = list(newState[2])

        # set the head and tail
        head = snake[0]
        tail = state[-1]


        # Position is the same and the env changes
        if action is LEFT:
            
            # Remove the very end of the snake
            snake.pop()
            
            # This is the optimization code for making the snakes body sorted (idk if this works yet but i think it should)
            if len(snake) != 0:
                #set the tail of the snake
                newtail = snake[-1]
                # remove the new tail
                snake.pop()
                # sort the body
                snake.sort()
                # insert the new tail
                snake.insert(-1, newtail)


            # insert the new head to the left
            snake.insert(0, (head[0]+LEFT[0], head[1]+LEFT[1]))        
        

            newState = [tuple(snake),tuple(foodList),tuple(obsList)]
            return tuple(newState)


        elif action is RIGHT:

            # Remove the very end of the snake
            snake.pop()
            
            # This is the optimization code for making the snakes body sorted (idk if this works yet but i think it should)
            if len(snake) != 0:

                #set the tail of the snake
                newtail = snake[-1]

                # remove the new tail
                snake.pop()

                # sort the body
                snake.sort()

                # insert the new tail
                snake.insert(-1, newtail)

            # insert the new head to the right
            snake.insert(0, (head[0]+RIGHT[0], head[1]+RIGHT[1]))        


            newState = [tuple(snake),tuple(foodList),tuple(obsList)]
            return tuple(newState)

        elif action is UP:

            # Remove the very end of the snake
            snake.pop()
            
            # This is the optimization code for making the snakes body sorted (idk if this works yet but i think it should)
            if len(snake) != 0:

                #set the tail of the snake
                newtail = snake[-1]

                # remove the new tail
                snake.pop()

                # sort the body
                snake.sort()

                # insert the new tail
                snake.insert(-1, newtail)


            # insert the new head
            snake.insert(0, (head[0]+UP[0], head[1]+UP[1]))
           
            newState = [tuple(snake),tuple(foodList),tuple(obsList)]
            return tuple(newState)

        elif action is DOWN:


            # Remove the very end of the snake
            snake.pop()
        
            # This is the optimization code for making the snakes body sorted (idk if this works yet but i think it should)
            if len(snake) != 0:

                #set the tail of the snake
                newtail = snake[-1]

                # remove the new tail
                snake.pop()

                # sort the body
                snake.sort()

                # insert the new tail
                snake.insert(-1, newtail)

            # insert the new head
            snake.insert(0, (head[0]+DOWN[0], head[1]+DOWN[1]))        

            newState = [tuple(snake),tuple(foodList),tuple(obsList)]
            return tuple(newState)
        
        newState = [tuple(snake),tuple(foodList),tuple(obsList)]
        return tuple(newState) 


    # Goal is if the head is in a food square if so its reached the goal
    def goal_test(self,state): 

        # Conversion Code from Tuple to Lists 
        # SnakeProblem((tuple(snakeList),tuple(foodList),tuple(obsList))
        newstate = list(state)

        snake = list(newstate[0])
        foodList = list(newstate[1])
        # set the head and tail
        head = snake[0]

        if head in foodList:
            return True
        return False

    # Path step cost
    def path_cost(self, c, state1, action, state2):

        return 1+self.total_cost


    # Calculate the closest food -- returns dist,cords i.e 7,(4,7)
    # calculates by manhattan distance
    def closest_food(self, state):
    
        # Conversion Code from Tuple to Lists 
        # SnakeProblem((tuple(snakeList),tuple(foodList),tuple(obsList))
        state = list(state)
        snake = list(state[0])
        foodList = list(state[1])

        # set the head and tail
        head = snake[0]

        # if the length of the foods is 0 then no closest
        if(len(foodList)==0):
            return 1
        # By default the closest food is the first one in the array
        # the calculation for distance is not correct atm
        closest = foodList[0]
        dist = int(math.hypot(closest[0] - head[0],closest[1] - head[1]))
        for i in foodList:
            hypot = int(math.hypot(i[0] - head[0],i[1] - head[1]))
            if dist > hypot:
                closest = i
                dist = hypot
        
        return dist


        

    # Caclulate the best food for distance -- returns dist,cord i.e 7,(4,7)
    # Calculation does distance / score 
    # Needs to be implemented
    def bestclosest_food(self, state):
        return (1,1)

    # Hueristic 1
    def h1(self,node):
        print(node)
        val = self.closest_food(node.state)
        return val

    # Hueristic 2
    def h2(self, node):
        return 1



    



    