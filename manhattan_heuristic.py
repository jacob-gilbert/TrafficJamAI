import copy
from queue import PriorityQueue


# print in visually nice form
def print_traffic_jam(matrix):
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] == 0:
                print("•", end = " ")
            else:
                identifier, vehicle, direction = matrix[row][col]
                print(identifier, end = " ")
        print()


# returns the upper/leftmost cell of red car and direction
def find_red_car(state):
    # Find the position of the red car (identifier = 0)
    for row in range(len(state)):
        for col in range(len(state[0])):
            if state[row][col] != 0:
                identifier, vehicle, direction = state[row][col]

                # Red car found
                if identifier == 0:  
                    return row, col, direction
    

# number of squares the red car has to move to get to the goal
def get_heuristic(state, goal):
    red_row, red_col, direction = find_red_car(state)
    goal_row, goal_col = goal

    # if direction is vertical
    if (direction == "v"):
        if (goal_row == 0):
            return red_row
        else:
            return len(state) - red_row - 2

    # if diection is horizontal
    else:
        if (goal_col == 0):
            return red_col
        else:
            return len(state[0] - red_col - 2)


# returns true if the current state n is the goal state
# the goal state is when the red car is in a cell bordering the exit 
def is_goal_state(state, goal):
    row, col = goal
    if state[row][col] != 0:
        identifier, vehicle, direction = state[row][col]

        # if red car is in the goal cell
        if (identifier == 0):
            return True

    return False


# returns a list of each of the neighboring states to the current state
# a neighbor state is the current state with an action
# an action is moving one vehicle 1 unit in a legal direction
def neighbors(current_state):
    vehicle_processed = [] # set for checking what vehicles have already been processed
    neighbors_list = []

    num_rows = len(current_state)
    num_cols = len(current_state[0]) 
    # loop through row of matrix left to right, then move down to next row
    for row in range(num_rows):
        for col in range(num_cols):

            # check if there is a vehicle in this cell
            if (current_state[row][col] != 0): 

                # parse
                identifier, vehicle, direction = current_state[row][col]

                # vehicle hasn't been processed yet
                if not (identifier in vehicle_processed):
                    
                    # add vehicle to set
                    vehicle_processed.append(identifier)

                    # if direction is horizontal
                    if direction == "h": 

                        # try move left (check if not at border and no vehicle to the left)
                        if (col != 0 and current_state[row][col - 1] == 0):

                            # create copy of matrix
                            next_state = copy.deepcopy(current_state)           

                            # move vehicle one unit to the left
                            next_state[row][col - 1] = current_state[row][col] 

                            # if vehicle is car
                            if (vehicle == "c"): 
                                next_state[row][col + 1] = 0 
                            else:
                                next_state[row][col + 2] = 0      

                            # add state to neighbors             
                            neighbors_list.append(next_state)

                        # for moving right, we need to know if it is a car or truck
                        if (vehicle == "c"):
                            # try move right (check if not at border and no vehicle to the right)
                            if (col + 2 < num_cols and current_state[row][col + 2] == 0):
                                
                                # create copy of matrix
                                next_state = copy.deepcopy(current_state)

                                # move car one unit to the right
                                next_state[row][col + 2] = current_state[row][col]
                                next_state[row][col] = 0
                                    
                                # add state to neighbors
                                neighbors_list.append(next_state)
                        else:
                            # try move right (check if not at border and no vehicle to the right)
                            if (col + 3 < num_cols and current_state[row][col + 3] == 0):
                                
                                # create copy of matrix
                                next_state = copy.deepcopy(current_state)

                                # move car one unit to the right
                                next_state[row][col + 3] = current_state[row][col]
                                next_state[row][col] = 0

                                # add state to neighbors
                                neighbors_list.append(next_state)

                    # direction is vertical
                    else: 

                        # try move up (check if not at border and no vehicle above)
                        if (row != 0 and current_state[row - 1][col] == 0):

                            # create copy of matrix
                            next_state = copy.deepcopy(current_state)   
                            
                            # move vehicle one unit up
                            next_state[row - 1][col] = current_state[row][col] 

                            # if vehicle is car
                            if (vehicle == "c"): 
                                next_state[row + 1][col] = 0 
                            else:
                                next_state[row + 2][col] = 0 

                            # add state to neighbors             
                            neighbors_list.append(next_state)
                        
                        # check if car as moving car down is different than moving truck down
                        if (vehicle == "c"):
                            
                            # try move down (check if not at border and no vehicle to the right)
                            if (row + 2 < num_rows and current_state[row + 2][col] == 0):
                                
                                # create copy of matrix
                                next_state = copy.deepcopy(current_state)

                                # move car one unit to the right
                                next_state[row + 2][col] = current_state[row][col]
                                next_state[row][col] = 0
                                    
                                # add state to neighbors
                                neighbors_list.append(next_state)
                        else:
                            # try move right (check if not at border and no vehicle to the right)
                            if (row + 3 < num_rows and current_state[row + 3][col] == 0):
                                
                                # create copy of matrix
                                next_state = copy.deepcopy(current_state)

                                # move car one unit to the right
                                next_state[row + 3][col] = current_state[row][col]
                                next_state[row][col] = 0

                                # add state to neighbors
                                neighbors_list.append(next_state)
                    
    return neighbors_list


# A* search
def astar_search(n, m, initial_state, goal):
    frontier = PriorityQueue() # priority queue
    tie_break = 0
    count_states = -1

    frontier.put((0 + get_heuristic(initial_state, goal), 0, tie_break, initial_state))  # (f, g, state)
    visited = set()
    #simple_print_jam(initial_state)

    while not frontier.empty():
        # Pop the state with the lowest f(n) = g(n) + h(n) 
        # where g(n) is actual cost to n, and h(n) if estimated cost from n to goal
        f, g, c, current_state = frontier.get()
        if str(current_state) in visited:
            continue
 
        count_states += 1

        # check if current state is a goal state
        if is_goal_state(current_state, goal):
            print("States Explored by Manhattan:", count_states)
            return g # return the actual cost to get to g

        visited.add(str(current_state)) # add current state to neighbors so we don't check again

        # Expand neighbors
        for neighbor in neighbors(current_state):
            if not (str(neighbor) in visited):
                tie_break += 1
                frontier.put((g + 1 + get_heuristic(neighbor, goal), g + 1, tie_break, neighbor)) # (f, g, state)

    return None