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
def move_car(r_bound, l_bound, col, front_row, car_id):
    moves_left = col - l_bound # this is the column we are in - where the left bound is
    moves_right = r_bound - (col + 1) # there are r_bound-1 column indexes so if col + 1 = r_bound we cannot move right
    
    if moves_left == 0 and moves_right == 0:
        print("here")
        return float('inf')
    
    
    # find the next part of the car
    if moves_right != 0: # checks if there is a column to the right of the red car
        if front_row[col + 1] == car_id:
            right = True
        else:
            right = False
    else:
        right = False

    # check how many squares the car needs to move out of the way to the right
    if right == True:
        if moves_right > 1: # check if the car can move one to the right in bounds
            right1 = front_row[col + 2]
            if right1 == 0: # if the space on the right is open we are done
                return 1
            elif right1[2] == "v":
                return 2
            else:
                if right1[1] == "c":
                    if moves_left > 1:
                        vehicle_loc = -1
                        for i in range(2):
                            if front_row[col - i - 1] != 0:
                                vehicle_loc =  i + 1
                                break
                        if vehicle_loc < 0:
                            return 2
                        else:
                            if front_row[col - vehicle_loc]  == "c":
                                return 2 + min(move_car(r_bound, col + 2, col + 2, front_row, front_row[col + 2]), move_car(col - vehicle_loc + 1, l_bound, col - vehicle_loc, front_row, front_row[col - vehicle_loc])) # have to consider moving left as well
                            else:
                                return 2 + min(move_car(r_bound, col + 2, col + 2, front_row, front_row[col + 2]), move_truck(col - vehicle_loc + 1, l_bound, col - vehicle_loc, front_row, front_row[col - vehicle_loc])) # truck on the left
                    else:
                        return 2 + move_car(r_bound, col + 2, col + 2, front_row, front_row[col + 2]) # only looking to the right
                else:
                    if moves_left > 0:
                        if front_row[col - 1][1] == "c":
                            return 2 + min(move_truck(r_bound, col + 2, col + 2,front_row, front_row[col + 2]), move_car(col, l_bound, col - 1, front_row, front_row[col - 1]))
                        else:
                            return 2 + min(move_truck(r_bound, col + 2, col + 2,front_row, front_row[col + 2]), move_truck(col, l_bound, col - 1, front_row, front_row[col - 1]))
                    else:
                        return 2 + move_truck(r_bound, col + 2, col + 2,front_row, front_row[col + 2])
        else:
            # can't move to the right so it must move 2 to the left
            # check if there is an open space to the left
            left1 = front_row[col - 1]
            left2 = front_row[col - 2]
            if left1 == 0:
                if left2 == 0:
                    return 2 # both squares are open
                elif left2[2] == "v":
                    return 3 # move verticle vehicle at least 1 square before moving 2 squares
                else:
                    if left2[1] == "c":
                        return 2 + move_car(col - 1, l_bound, col - 2, front_row, left2)
                    else:
                        return 2 + move_truck(col - 1, l_bound, col - 2, front_row, left2)
            elif left1[2] == "v":
                if left2 == 0:
                    return 3 # move verticle vehicle and then 2 squares
                elif left2[2] == "v":
                    return 4 # move both verticle vehicles and then 2 squares
                else:
                    if left2[1] == "c":
                        return 3 + move_car(col - 1, l_bound, col - 2, front_row, left2)
                    else:
                        return 3 + move_truck(col - 1, l_bound, col - 2, front_row, left2)
            else:
                if left1[1] == "c":
                    return 2 + move_car(col, l_bound, col - 1, front_row, left1)
                else:
                    return 2 + move_truck(col, l_bound, col - 1, front_row, left1)
                
    else:
        if moves_left > 1: # check if the car can move one to the right in bounds
            left1 = front_row[col - 2]
            if left1 == 0: # if the space on the right is open we are done
                return 1
            elif left1[2] == "v":
                return 2
            else:
                if left1[1] == "c":
                    if moves_right > 1:
                        vehicle_loc = -1
                        for i in range(2):
                            if front_row[col + i + 1] != 0:
                                vehicle_loc = i + 1
                                break
                        if vehicle_loc < 0:
                            return 2
                        else:
                            if front_row[col + vehicle_loc][1] == "c":
                                return 2 + min(move_car(col - 1, l_bound, col - 2, front_row, front_row[col - 2]), move_car(r_bound, col + vehicle_loc, col + vehicle_loc, front_row, front_row[col + vehicle_loc])) # have to consider moving right as well
                            else:
                                return 2 + min(move_car(col - 1, l_bound, col - 2, front_row, front_row[col - 2]), move_truck(r_bound, col + vehicle_loc, col + vehicle_loc, front_row, front_row[col + vehicle_loc])) # truck on the right
                    else:
                        return 2 + move_car(col - 1, l_bound, col - 2, front_row, front_row[col - 2]) # only looking to the left
                else:
                    if moves_right > 0:
                        if front_row[col + 1][1] == "c":
                            return 2 + min(move_truck(col - 1, l_bound, col - 2,front_row, front_row[col - 2]), move_car(r_bound, col + 1, col + 1, front_row, front_row[col + 1]))
                        else:
                            return 2 + min(move_truck(col - 1, l_bound, col - 2,front_row, front_row[col - 2]), move_truck(r_bound, col + 1, col + 1, front_row, front_row[col + 1]))
                    else:
                        return 2 + move_truck(col - 1, l_bound, col - 2,front_row, front_row[col - 2])
        else:
            # can't move to the left so it must move 2 to the right
            # check if there is an open space to the left
            right1 = front_row[col + 1]
            right2 = front_row[col + 2]
            if right1 == 0:
                if right2 == 0:
                    return 2 # both squares are open
                elif right2[2] == "v":
                    return 3 # move verticle vehicle at least 1 square before moving 2 squares
                else:
                    if right2[1] == "c":
                        return 2 + move_car(r_bound, col + 2, col + 2, front_row, right2)
                    else:
                        return 2 + move_truck(r_bound, col + 2, col + 2, front_row, right2)
            elif right1[2] == "v":
                if right2 == 0:
                    return 3 # move verticle vehicle and then 2 squares
                elif right2[2] == "v":
                    return 4 # move both verticle vehicles and then 2 squares
                else:
                    if right2[1] == "c":
                        return 3 + move_car(r_bound, col + 2, col + 2, front_row, right2)
                    else:
                        return 3 + move_truck(r_bound, col + 2, col + 2, front_row, right2)
            else:
                if right1[1] == "c":
                    return 2 + move_car(r_bound, col + 2, col + 1, front_row, right1)
                else:
                    return 2 + move_truck(r_bound, col + 2, col + 1, front_row, right1)



def move_truck(r_bound, l_bound, col, front_row, truck_id):
    moves_left = col - l_bound # this is the column we are in - where the left bound is
    moves_right = r_bound - (col + 1) # there are r_bound-1 column indexes so if col + 1 = r_bound we cannot move right
    
    if moves_left == 0 and moves_right == 0:
        return float('inf')
    
    # find the next two parts of the truck
    if moves_right > 0: # checks if there is a column to the right in front of the red car
        if front_row[col + 1] == truck_id:
            right = True
        else:
            right = False
    else:
        right = False
        left = True
    if moves_left > 0: # checks if there is a column to the left in front of the red car
        if front_row[col - 1] == truck_id:
            left = True
        else:
            left = False
    else:
        left = False


    if left and right: # truck must occupy square in front of red car and above to the right and left by 1
        # the truck must move 2 squares either left or right
        # check the boundaries of left and right
        if moves_right > 2 and moves_left > 2:
            # at this point we know we need to move the truck 2 squares, see any additional affects of trying to get right
            right1 = front_row[col + 2]
            right2 = front_row[col + 3]
            add_moves_right = 0
            hn_right = 0
            
            if right1 != 0:
                if right1[2] == "v":
                    add_moves_right += 1
                else:
                    if right1[1] == "c": # right2 must also be a car
                        hn_right = 2 + move_car(r_bound, col + 2, col + 2, front_row, right1)
                    else: # right2 must also be a truck
                        hn_right = 2 + move_truck(r_bound, col + 2, col + 2, front_row, right1)
            if right2 != 0:
                if right2[2] == "v":
                    add_moves_right += 1
                else:
                    if right1 == 0:
                        if right2[1] == "c":
                            hn_right = 2 + move_car(r_bound, col + 2, col + 2, front_row, right1)
                        else:
                            hn_right = 2 + move_truck(r_bound, col + 2, col + 2, front_row, right1)
            if right1 == 0 and right2 == 0:
                hn_right = 2
                
            # see any additional affects of trying to move left
            left1 = front_row[col - 2]
            left2 = front_row[col - 3]
            add_moves_left = 0
            
            if left1 != 0:
                if left1[2] == "v":
                    add_moves_left += 1
                else:
                    if left1[1] == "c": # left2 must also be a car
                        hn_left = 2 + move_car(col - 1, l_bound, col - 2, front_row, left1)
                    else:
                        hn_left = 2 + move_truck(col - 1, l_bound, col - 2, front_row, left1)
            if left2 != 0:
                if left2[2] == "v":
                    add_moves_left += 1
                else:
                    if left1 == 0:
                        if left2[1] == "c":
                            hn_left = 2 + move_car(col - 1, l_bound, col - 2, front_row, right1)
                        else:
                            hn_left = 2 + move_truck(col - 1, l_bound, col - 2, front_row, right1)
            if left1 == 0 and left2 == 0:
                hn_left = 2
            
            return min(hn_left + add_moves_left, hn_right + add_moves_right)
            
            
        elif moves_left > 2: # cannot go right
            # see any additional affects of trying to move left
            left1 = front_row[col - 2]
            left2 = front_row[col - 3]
            add_moves_left = 0
            hn_left = 0
            
            if left1 != 0:
                if left1[2] == "v":
                    add_moves_left += 1
                else:
                    if left1[1] == "c": # left2 must also be a car
                        hn_left = 2 + move_car(col - 1, l_bound, col - 2, front_row, left1)
                    else:
                        hn_left = 2 + move_truck(col - 1, l_bound, col - 2, front_row, left1)
            if left2 != 0:
                if left2[2] == "v":
                    add_moves_left += 1
                else:
                    if left1 == 0:
                        if left2[1] == "c":
                            hn_left = 2 + move_car(col - 1, l_bound, col - 2, front_row, left2)
                        else:
                            hn_left = 2 + move_truck(col - 1, l_bound, col - 2, front_row, left2)
            if left1 == 0 and left2 == 0:
                return 2
            return hn_left + add_moves_left
        
        
        
        else: # cannot go left
            # see any additional affects of trying to get right
            right1 = front_row[col + 2]
            right2 = front_row[col + 3]
            add_moves_right = 0
            hn_right = 0
            
            if right1 != 0:
                if right1[2] == "v":
                    add_moves_right += 1
                else:
                    if right1[1] == "c": # right2 must also be a car
                        hn_right = 2 + move_car(r_bound, col + 2, col + 2, front_row, right1)
                    else: # right2 must also be a truck
                        hn_right = 2 + move_truck(r_bound, col + 2, col + 2, front_row, right1)
            if right2 != 0:
                if right2[2] == "v":
                    add_moves_right += 1
                else:
                    if right1 == 0 or add_moves_right > 0:
                        if right2[1] == "c":
                            hn_right = 2 + move_car(r_bound, col + 2, col + 2, front_row, right2)
                        else:
                            hn_right = 2 + move_truck(r_bound, col + 2, col + 2, front_row, right2)
            if right1 == 0 and right2 == 0:
                return 2
            return hn_right + moves_right
            
            

    elif left and not right: # truck must occupy square in front of red car and above to the left * 2
        if moves_right > 2 and moves_left > 2:
            right1 = front_row[col + 1]
            right2 = front_row[col + 2]
            right3 = front_row[col + 3]
            add_moves_right = 0
            hn_right = 0
            
            if right1 != 0:
                if right1[2] == "v":
                    add_moves_right += 1
                else:
                    if right1[1] == "c":
                        hn_right = 2 + move_car(r_bound, col + 1, col + 1, front_row, right1)
                    else:
                        hn_right = 2 + move_truck(r_bound, col + 1, col + 1, front_row, right1)
            if right2 != 0:
                if right2[2] == "v":
                    add_moves_right += 1
                else:
                    if right1 == 0 or add_moves_right > 0:
                        if right2[1] == "c":
                            hn_right = 2 + move_car(r_bound, col + 2, col + 2, front_row, right2)
                        else:
                            hn_right = 2 + move_truck(r_bound, col + 2, col + 2, front_row, right2)
            if right3 != 0:
                if right3[2] == "v":
                    add_moves_right += 1
                else:
                    if right2 == 0 or add_moves_right > 1:
                        if right3[1] == "c":
                            hn_right = 2 + move_car(r_bound, col + 3, col + 3, front_row, right3)
                        else:
                            hn_right = 2 + move_truck(r_bound, col + 3, col + 3, front_row, right3)
            
            if right1 == 0 and right2 == 0 and right3 == 0:
                hn_right = 3
            
            left1 = front_row[col - 3]
            if left1 == 0:
                return 1
            else:
                if left1[2] == "v":
                    return 2
                else:
                    if left1[1] == "c":
                        hn_left = 2 + move_car(col - 2, l_bound, col - 3, front_row, left1)
                    else:
                        hn_left = 2 + move_truck(col - 2, l_bound, col - 3, front_row, left1)
                        
            return min(hn_left, hn_right + add_moves_right)
        
        elif moves_left > 2: # cannot move right
            left1 = front_row[col - 3]
            if left1 == 0:
                return 1
            else:
                if left1[2] == "v":
                    return 2
                else:
                    if left1[1] == "c":
                        return 2 + move_car(col - 2, l_bound, col - 3, front_row, left1)
                    else:
                        return 2 + move_truck(col - 2, l_bound, col - 3, front_row, left1)
        
        else: # cannot move left
            right1 = front_row[col + 1]
            right2 = front_row[col + 2]
            right3 = front_row[col + 3]
            add_moves_right = 0
            hn_right = 0
            
            if right1 != 0:
                if right1[2] == "v":
                    add_moves_right += 1
                else:
                    if right1[1] == "c":
                        hn_right = 2 + move_car(r_bound, col + 1, col + 1, front_row, right1)
                    else:
                        hn_right = 2 + move_truck(r_bound, col + 1, col + 1, front_row, right1)
            if right2 != 0:
                if right2[2] == "v":
                    add_moves_right += 1
                else:
                    if right1 == 0 or add_moves_right > 0:
                        if right2[1] == "c":
                            hn_right = 2 + move_car(r_bound, col + 2, col + 2, front_row, right2)
                        else:
                            hn_right = 2 + move_truck(r_bound, col + 2, col + 2, front_row, right2)
            if right3 != 0:
                if right3[2] == "v":
                    add_moves_right += 1
                else:
                    if right2 == 0 or add_moves_right > 1:
                        if right3[1] == "c":
                            hn_right = 2 + move_car(r_bound, col + 3, col + 3, front_row, right3)
                        else:
                            hn_right = 2 + move_truck(r_bound, col + 3, col + 3, front_row, right3)
            
            if right1 == 0 and right2 == 0 and right3 == 0:
                return 3   
            return hn_right + add_moves_right
            
    else: # right and not left --> truck must occupy square in front of red car and above to the right * 2
        if moves_right > 2 and moves_left > 2:
            left1 = front_row[col - 1]
            left2 = front_row[col - 2]
            left3 = front_row[col - 3]
            add_moves_left = 0
            hn_left = 0
                
            if left1 != 0:
                if left1[2] == "v":
                    add_moves_leftt += 1
                else:
                    if left1[1] == "c":
                        hn_left = 2 + move_car(col, l_bound, col - 1, front_row, left1)
                    else:
                        hn_left = 2 + move_truck(col, l_bound, col - 1, front_row, left1)
            if left2 != 0:
                if left2[2] == "v":
                    add_moves_left += 1
                else:
                    if left1 == 0 or add_moves_left > 0:
                        if left2[1] == "c":
                            hn_left = 2 + move_car(col - 1, l_bound, col - 2, front_row, left2)
                        else:
                            hn_left = 2 + move_truck(col - 1, l_bound, col - 2, front_row, left2)
            if left3 != 0:
                if left3[2] == "v":
                    add_moves_left += 1
                else:
                    if left2 == 0 or add_moves_left > 1:
                        if left3[1] == "c":
                            hn_left = 2 + move_car(col - 2, l_bound, col - 3, front_row, left3)
                        else:
                            hn_left = 2 + move_truck(col - 2, l_bound, col - 3, front_row, left3)
                
            if left1 == 0 and left2 == 0 and left3 == 0:
                hn_left = 3   
                
            right1 = front_row[col + 3]
            if right1 == 0:
                return 1
            else:
                if right1[2] == "v":
                    return 2
                else:
                    if right1[1] == "c":
                        hn_right = 2 + move_car(r_bound, col + 3, col + 3, front_row, right1)
                    else:
                        hn_right = 2 + move_truck(r_bound, col + 3, col + 3, front_row, right1)
                        
            return min(hn_right, hn_left + add_moves_left)
        
        elif moves_left > 2: # cannot move right
            left1 = front_row[col - 1]
            left2 = front_row[col - 2]
            left3 = front_row[col - 3]
            add_moves_left = 0
            hn_left = 0
                
            if left1 != 0:
                if left1[2] == "v":
                    add_moves_leftt += 1
                else:
                    if left1[1] == "c":
                        hn_left = 2 + move_car(col, l_bound, col - 1, front_row, left1)
                    else:
                        hn_left = 2 + move_truck(col, l_bound, col - 1, front_row, left1)
            if left2 != 0:
                if left2[2] == "v":
                    add_moves_left += 1
                else:
                    if left1 == 0 or add_moves_left > 0:
                        if left2[1] == "c":
                            hn_left = 2 + move_car(col - 1, l_bound, col - 2, front_row, left2)
                        else:
                            hn_left = 2 + move_truck(col - 1, l_bound, col - 2, front_row, left2)
            if left3 != 0:
                if left3[2] == "v":
                    add_moves_left += 1
                else:
                    if left2 == 0 or add_moves_left > 1:
                        if left3[1] == "c":
                            hn_left = 2 + move_car(col - 2, l_bound, col - 3, front_row, left3)
                        else:
                            hn_left = 2 + move_truck(col - 2, l_bound, col - 3, front_row, left3)
                
            if left1 == 0 and left2 == 0 and left3 == 0:
                return 3
            return hn_left + add_moves_left
        
        else:
            right1 = front_row[col + 3]
            if right1 == 0:
                return 1
            else:
                if right1[2] == "v":
                    return 2
                else:
                    if right1[1] == "c":
                        return 2 + move_car(r_bound, col + 3, col + 3, front_row, right1)
                    else:
                        return 2 + move_truck(r_bound, col + 3, col + 3, front_row, right1)


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
                        return min(hn, move_car(m, 0, col, neighbor_state[row - i - 1], front_of_car)) + row
                    else:
                        return min(hn, move_truck(m, 0, col, neighbor_state[row - i - 1], front_of_car)) + row
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
        #print("Current State:")
        #simple_print_jam(current_state)
        #print("\n")
        count_states += 1

        # check if current state is a goal state
        if is_goal_state(current_state, goal):
            print("States popped advanced h(n):", count_states)
            # Reconstruct the path from goal to start
            path = []
            while current_state is not None:
                path.append(current_state)
                current_state = parent[str(current_state)]
            path.reverse()  # reverse the path to start from the initial state
            return path, g  # return the path and cost
            # return g # return the actual cost to get to g

        visited.append(current_state) # add current state to neighbors so we don't check again

        # Expand neighbors
        for neighbor in neighbors(current_state):
            if not (neighbor in visited):
                tie_break += 1
                frontier.put((g + 1 + get_heuristic(n, m, neighbor), g + 1, tie_break, neighbor)) # (f, g, state)
                if str(neighbor) not in parent:  # only set the parent if it hasn't been visited
                    parent[str(neighbor)] = current_state
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