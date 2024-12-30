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
