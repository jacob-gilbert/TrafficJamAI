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


# This is a helper function of get_heuristic which calculates h(n).
# move_car gets called to figure out how far a car in front of the red car needs to be moved.
# If the car cannot move without hitting something else it will calculate the minimum additonal
# moves of moving the first obstacle in car's way.
def move_car(m, row, col, front_row, car_id):
    # find the next part of the car
    if col + 1 != m: # checks if there is a column to the right of the red car
        if front_row[col + 1] == car_id:
            right = True
        else:
            right = False
    else:
        right = False

    # check how many squares the car needs to move out of the way to the right and left
    if right == True:
        if col + 2 != m: # check if the car can move one to the right in bounds
            
            # check if anything is in its way on the right
            if front_row[col + 1][2] != 0: # look at the first square to the right of the blocking car, if its not zero something will have to move
                return 2 + row
            else:
                return 1 + row
                
        else:
            # can't move to the right so it must move 2 to the left
            
            # check if anything is in it's way
            first_in_front = front_row[col - 1] # look at the first square to the left of the blocking car
            if first_in_front != 0:
                if first_in_front[2] == "v": # a verticle vehicle will have to move at least one square out of the way
                    return 3 + row
                else: # the vehicle is horizontal so it will have to move 2 spaces out of the way
                    return 4 + row
            else: # space is open
                second_in_front = front_row[col - 2]
                if second_in_front != 0:
                     # if the second spot is not open whatever there will have to move at least 1 square
                    return 3 + row
                else:
                    return 2 + row
    else:
        if col - 2 >= 0: # check if the car can move one to the left in bounds
            
            # check if anything is in its way on the left
            if front_row[col - 1][2] != 0: # look at the first square to the left of the blocking car, if its not zero something will have to move
                return 2 + row
            else:
                return 1 + row
            
        else:
            # can't move to the left so it must move 2 to the right
            
            # check if anything is in it's way
            first_in_front = front_row[col + 1] # look at the first square to the right of the blocking car
            if first_in_front != 0:
                if first_in_front[2] == "v": # a verticle vehicle will have to move at least one square out of the way
                    return 3
                else: # the vehicle is horizontal so it will have to move 2 spaces out of the way
                    return 4
            else: # space is open
                second_in_front = front_row[col + 2]
                if second_in_front != 0:
                    # if the second spot is not open whatever there will have to move at least 1 square
                    return 3 + row
                else:
                    return 2 + row
                

# this is a helper function of get_heuristic which calculates h(n)
# move_truck gets called to figure out how far a truck in front of the red car needs to be moved
# if the truck cannot move without hitting something else it will calculate the minimum additonal
# moves of moving the first obstacle in truck's way
def move_truck(m, row, col, front_row, truck_id):
    # find the next two parts of the truck
    if col + 1 != m: # checks if there is a column to the right in front of the red car
        if front_row[col + 1] == truck_id:
            right = True
        else:
            right = False
    else:
        right = False
        left = True
    if col - 1 >= 0: # checks if there is a column to the left in front of the red car
        if front_row[col - 1] == truck_id:
            left = True
        else:
            left = False
    else:
        left = False

    if left and right: # truck must occupy square in front of red car and above to the right and left by 1
        # the truck must move 2 squares either left or right
        # check the boundaries of left and right
        if col + 3 < m:
            if col - 3 >= 0:
                # the truck can move in bounds 2 squares in either direction
                return 2 + row
            else:
                # can't move left in bounds 2 squares so only look right
                right_of_t = front_row[col + 2]
                if right_of_t != 0:
                    if right_of_t[2] == "v":
                        # something verticle has to move at least 1 space out of way and truck moves 2
                        return 3 + row
                    else:
                        # something horizontal has to move at least 2 spaces out of the way of truck and truck moves 2
                        return 4 + row
                else:
                    # right of the truck is open
                    if front_row[col + 3] != 0:
                        # anything in the this square will have to move at least 1 away and truck moves 2
                        return 3 + row
                    else:
                        return 2 + row
        else:
            # can't move left in bounds 2 squares so only look right
            left_of_t = front_row[col - 2]
            if left_of_t != 0:
                if left_of_t[2] == "v":
                    # something verticle has to move at least 1 space out of way and truck moves 2
                    return 3 + row
                else:
                    # something horizontal has to move at least 2 spaces out of the way of truck and truck moves 2
                    return 4 + row
            else:
                # right of the truck is open
                if front_row[col - 3] != 0:
                    # anything in the this square will have to move at least 1 away and truck moves 2
                    return 3 + row
                else:
                    return 2 + row

    elif left and not right: # truck must occupy square in front of red car and above to the left * 2
        if col - 3 >= 0: # check if there is a column three to the left of the red car, means there will be room for the truck to move
            if front_row[col - 3] != 0:
                # if something occupies the space to the left, have to move it first and then truck
                return 2 + row
            else:
                # if the space to the left is open, only have to move the truck by 1
                return 1 + row
        else:
            # assuming nothing else is in the way, but lets check
            right1_of_t = front_row[col + 1]
            if right1_of_t != 0:
                if right1_of_t[2] == "v":
                    # something verticle has to move at least 1 space out of way
                    return 4 + row
                else:
                    # something horizontal has to move at least 3 spaces out of the way of truck
                    return 6 + row
            else: # space open check next one
                right2_of_t = front_row[col + 2]
                if right2_of_t != 0:
                    if right2_of_t[2] == "v":
                        # something verticle has to move at least 1 space out of way
                        return 4 + row
                    else:
                        # something horizontal has to move at least 3 spaces out of the way of truck
                        return 5 + row
                else: # space open check third one
                    if front_row[col + 2] != 0:
                        # anything in this square will have to move at least 1 square at of the way regardless of direction
                        return 4 + row
                    else:
                        return 3
            
    else: # right and not left --> truck must occupy square in front of red car and above to the right * 2
        if col + 3 >= m: # check if there is a column three to the right of the red car, means there will be room for the truck to move
            if front_row[col + 3] != 0:
                # if something occupies the space to the left, have to move it first and then truck
                return 2 + row
            else:
                # if the space to the left is open, only have to move the truck by 1
                return 1 + row
        else:
            r_not_l = 3 # assuming nothing else is in the way, but lets check
            left1_of_t = front_row[col - 1]
            if left1_of_t != 0:
                if left1_of_t[2] == "v":
                    # something verticle has to move at least 1 space out of way
                    return 4 + row
                else:
                    # something horizontal has to move at least 3 spaces out of the way of truck
                    return 6
            else: # space open check next one
                left2_of_t = front_row[col - 2]
                if left2_of_t != 0:
                    if left2_of_t[2] == "v":
                        # something verticle has to move at least 1 space out of way
                        return 4 + row
                    else:
                        # something horizontal has to move at least 3 spaces out of the way of truck
                        return 5 + row
                else: # space open check third one
                    if front_row[col + 2] != 0:
                        # anything in this square will have to move at least 1 square at of the way regardless of direction
                        return 4
                    else:
                        return 3
    

# returns h(n): the estimated cost from current node n to the goal
# based off some heuristic
# second obstacle heuristic
def get_heuristic(n, m, neighbor_state):
    # the for loops always go from top left to bottom right:
    hn = float('inf')
    for row in range(n):
        for col in range(m):
            if neighbor_state[row][col] == (0,"c","v"): # this will always be the top square of the red car
                for i in range(row): # go until you find the first obstacle, if you don't you'll reach the goal
                    front_of_car = neighbor_state[row - i - 1][col] # this is the square above the red car
                    if front_of_car == 0:
                        continue # no obstacle yet
                    elif front_of_car[1] == "c":
                        return min(hn, move_car(m, row, col, neighbor_state[row - i - 1], front_of_car)) # looks at every row above the red car and takes the minimum hn from every row
                    else:
                        return min(hn, move_truck(m, row, col, neighbor_state[row - i - 1], front_of_car))
                if hn == float('inf'):
                    return row # no obstacles just true distance to goal
                else:
                    return hn
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
    parent = {}  # to track the parent of each state

    frontier.put((0 + get_heuristic(n, m, initial_state), 0, tie_break, initial_state))  # (f, g, state)
    visited = []
    parent[str(initial_state)] = None  # initial state has no parent

    while(not frontier.empty()):
        # Pop the state with the lowest f(n) = g(n) + h(n) 
        # where g(n) is actual cost to n, and h(n) if estimated cost from n to goal
        f, g, c, current_state = frontier.get()
        
        if current_state in visited:
            continue
        
        count_states += 1

        # check if current state is a goal state
        if is_goal_state(current_state, goal):
            print("States Explored by Move_the_Obstacle:", count_states)
            # Reconstruct the path from goal to start
            path = []
            while current_state is not None:
                path.append(current_state)
                current_state = parent[str(current_state)]
            path.reverse()  # reverse the path to start from the initial state
            return path, g  # return the path and cost

        visited.append(current_state) # add current state to neighbors so we don't check again

        # Expand neighbors
        for neighbor in neighbors(current_state):
            if not (neighbor in visited):
                tie_break += 1
                frontier.put((g + 1 + get_heuristic(n, m, neighbor), g + 1, tie_break, neighbor)) # (f, g, state)
                if str(neighbor) not in parent:  # only set the parent if it hasn't been visited
                    parent[str(neighbor)] = current_state
    return None