import copy
from queue import PriorityQueue

def read_matrix_from_file(filename):
    with open(filename, 'r') as file:
        # Read the first line to get the dimensions
        first_line = file.readline().strip()
        
        # split the first line into two parts and turn each into an integer
        n, m = map(int, first_line.split())
        
        # Initialize an empty matrix
        matrix = []

        # Read the next n lines for the matrix data
        for i in range(n):
            row = list(map(str, file.readline().strip().split()))
            matrix.append(row)

    return n, m, matrix

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

def simple_print_jam(matrix):
    for row in matrix:
        print(row)


# returns the upper/leftmost cell of red car and direction
def find_red_car(state):
    # Find the position of the red car (identifier = 0)
    red_car_row = None
    red_car_col = None
    for row in range(len(state)):
        for col in range(len(state[0])):
            if state[row][col] != 0:
                identifier, vehicle, direction = state[row][col]

                # Red car found
                if identifier == 0:  
                    return row, col, direction



# this is a helper function of get_heuristic which calculates h(n)
# move_car gets called to figure out how far a car in front of the red car needs to be moved
def move_car(m, row, col, front_row, car_id):
    # find the next part of the car
    if col + 1 != m: # checks if there is a column to the right of the red car
        if front_row[col + 1] == car_id:
            right = True
        else:
            right = False
    else:
        right = False

    # check how many squares the car needs to move out of the way to the right
    count_open_right = 0
    count_open_left = 0
    if right == True:
        if col + 2 != m: # check if the car can move one to the right in bounds
            count_open_right += 1
        else:
            count_open_left += 2 # can't move to the right so it must move 2 to the left
    else:
        if col - 2 >= 0: # check if the car can move one to the left in bounds
            count_open_left += 1
        else:
            count_open_right += 2 # can't move to the left so it must move 2 to the right
                    
    return max(count_open_left, count_open_right) + row


def move_truck(m, row, col, front_row, truck_id):
    # find the next part of the car
    if col + 1 != m: # checks if there is a column to the right in front of the red car
        if front_row[col + 1] == truck_id:
            right = True
        else:
            right = False
    else:
        right = False
    if col - 1 >= 0: # checks if there is a column to the left in front of the red car
        if front_row[col - 1] == truck_id:
            left = True
        else:
            left = False
    else:
        left = False

    l_and_r = 0
    l_not_r = 0
    r_not_l = 0
    if left and right: # truck must occupy square in front of red car and above to the right and left by 1
        l_and_r = 2
    elif left and not right: # truck must occupy square in front of red car and above to the left * 2
        if col - 3 >= 0: # check if there is a column three to the left of the red car, means there will be room for the truck to move
            l_not_r = 1
        else:
            l_not_r = 3
    else: # right and not left --> truck must occupy square in front of red car and above to the right * 2
        if col + 3 >= m: # check if there is a column three to the right of the red car, means there will be room for the truck to move
            r_not_l = 1
        else:
            r_not_l = 3
    return max(l_and_r, l_not_r, r_not_l) + row
    

# returns h(n): the estimated cost from current node n to the goal
# based off some heuristic
def get_heuristic(n, m, neighbor_state):
    # the for loops always go from top left to bottom right:
    for row in range(n):
        for col in range(m):
            if neighbor_state[row][col] == (0,"c","v"): # this will always be the top square of the red car
                front_of_car = neighbor_state[row - 1][col] # this is the square above the red car
                for i in range(row): # go until you find the first obstacle, if you don't you'll reach the goal
                    if front_of_car == 0:
                        continue # no obstacle yet
                    elif front_of_car[1] == "c":
                        return move_car(m, row, col, neighbor_state[row - i - 1], front_of_car)
                    else:
                        return move_truck(m, row, col, neighbor_state[row - i - 1], front_of_car)
                return row # no obstacles just true distance til goal
    return -1


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

    frontier.put((0 + get_heuristic(n, m, initial_state), 0, tie_break, initial_state))  # (f, g, state)
    visited = []

    while(not frontier.empty()):
        # Pop the state with the lowest f(n) = g(n) + h(n) 
        # where g(n) is actual cost to n, and h(n) if estimated cost from n to goal
        f, g, c, current_state = frontier.get()
        
        if current_state in visited:
            continue
        #print("Current State:")
        #simple_print_jam(current_state)
        #print("\n")
        count_states += 1

        # check if current state is a goal state
        if is_goal_state(current_state, goal):
            print("States popped less simple h(n):", count_states)
            return g # return the actual cost to get to g

        visited.append(current_state) # add current state to neighbors so we don't check again

        # Expand neighbors
        for neighbor in neighbors(current_state):
            if not (neighbor in visited):
                tie_break += 1
                frontier.put((g + 1 + get_heuristic(n, m, neighbor), g + 1, tie_break, neighbor)) # (f, g, state)

    return None


initial_state = [   [0,             0,              0,              0,              0               ],
                    [(1, "c", "h"), (1, "c", "h"),   0,             0,              0               ],
                    [(2, "c", "v"), 0,              0,              (3, "c", "h"),  (3, "c", "h")   ],
                    [(2, "c", "v"), (4, "c", "h"), (4, "c", "h"),  0,              (0, "c", "v")   ],
                    [(5, "t", "h"), (5, "t", "h"),  (5, "t", "h"),  0,              (0, "c", "v")   ]
                ]

n = 5
m = 5
goal = (0, 4)

#print(astar_search(n, m, initial_state, goal))





#filename = 'traffic_jam_input.txt'
#n, m, matrix = read_matrix_from_file(filename)
#print_traffic_jam(matrix)