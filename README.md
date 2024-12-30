# README

The code is written in python. Download the folder. The heuristics have been imported into practice_heuristic.py. The three example intitial states are in the practice_heuristic.py file to show the expected input for an initial state along with the attributes that need to be used with them, such as the number of rows, n, the number of columns m, and the goal state location.

To run the python code, run python practice_heuristic.py in the proper directory.

## Format for the initial state:

- 2d matrix
- empty cells have a 0
- cells with a vehicle have a tuple
- The red car must be labeled (0, "c", "v")
- Tuple: (id, vehicle_type, vehicle direction)
- A single car will have the same id in both of its tuples to know that they are the same car
- Vehicle type is either “c” for car or “t” for truck
- Direction is either “v” for vertical or “h” for horizontal
- Example row [0,&emsp;0,&emsp;(1, “c”, “h”),&emsp;(1, “c”, “h”),&emsp;0]

## Output

- Outputs total states explored/goal tested by Manhattan Heuristic and Move The Obstacle Heuristic
- Outputs total solution cost that both heuristics find
- The Move the Obstacle Heuristic also outputs the path from the initial state to the goal state

## Heuristic Explanation

*Manhatten Distance*
- The manhatten distance is the distance between two points in a grid, which is relevant for this problem because the only possible movements are up, down, left, and right. Diagonal moves are not allowed. The determined Manhatten distance will always assume an open path from the red car to the end state and won't account for other vehicles blocking the red car's path. Thus, the manhatten distance is always the minimum amount of moves to get the red car from the its initial state to its final state; therefore guarenteeing the heuristic will be admissible.

*Traffic Jam*
- This heuristic calculates how far one vehicle in front of the red car needs to be moved to free the space for the red car (when there is a vehicle there) and adds this distance to the manhatten distance of the red car to the end state. This calculation is always the minimum amount of moves required when there is one vehicle in the red car's way, so the heuristic is always admissible.

*Move the Obstacle*
- Similarly to traffic jam it calculates moving a vehicle in front of the red car, but can also move a vehicle blocking that first obstacle vehicle.

*Line*
- This calculates how many moves it takes to clear an entire line of obstacles depending on how many are present. When there is an obstacle it recursively centers at that obstacle and attempts to move it, if it can move to an open space then it moves the obstacle, but if it is also blocked it makes another recursive call and continues to do so until an open space is found or the end of the board is reached. For vehicles in the vertical direction it just assumes it must be moved one tile, but for horizontal vehicles it can determine the exact amount it must move.