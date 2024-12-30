import manhattan_heuristic
import move_the_obstacle_heuristic


# initial state A

initial_state = [   [0,             0,              0,              (4, "c", "v"),  (5, "c", "h"),  (5, "c", "h")],
                    [0,             0,              0,              (4, "c", "v"),  (2, "c", "h"),  (2, "c", "h")],
                    [(1, "c", "v"), (7, "t", "h"),  (7, "t", "h"),  (7, "t", "h"),  (3, "c", "h"),  (3, "c", "h")],
                    [(1, "c", "v"), 0,              0,              0,              0,              (0, "c", "v")],
                    [0,             0,              (6, "t", "h"),  (6, "t", "h"),  (6, "t", "h"),  (0, "c", "v")],
                    [0,             0,              0,              0,              0,              0            ]]
n = 6
m = 6
goal = (0,5)

cost = manhattan_heuristic.astar_search(n, m, initial_state, goal)
print("Solution Cost:", cost, "\n")

path, cost = move_the_obstacle_heuristic.astar_search(n, m, initial_state, goal)
print("Solution Cost:", cost)
print("Printing Path:")
for state in path:
    move_the_obstacle_heuristic.print_traffic_jam(state)
    print()



"""# initial state B

initial_state = [   [(1, "t", "v"), (2, "t", "v"),  (6, "c", "v"),  (3, "t", "h"),  (3, "t", "h"),  (3, "t", "h")],
                    [(1, "t", "v"), (2, "t", "v"),  (6, "c", "v"),  (4, "t", "h"),  (4, "t", "h"),  (4, "t", "h")],
                    [(1, "t", "v"), (2, "t", "v"),  (7, "c", "h"),  (7, "c", "h"),  (9, "c", "h"),  (9, "c", "h")],
                    [(5, "c", "h"), (5, "c", "h"),  0,              0,              (0, "c", "v"),  0            ],
                    [0,             0,              0,              0,              (0, "c", "v"),  0            ],
                    [0,             0,              (8, "c", "h"),  (8, "c", "h"),  0,              0            ]]
n = 6
m = 6
goal = (0,4)

print(manhattan_heuristic.astar_search(n, m, initial_state, goal))

path, g = move_the_obstacle_heuristic.astar_search(n, m, initial_state, goal)
for state in path:
    move_the_obstacle_heuristic.print_traffic_jam(state)
print(g)"""



"""initial_state = [   [0,             0,              (2, "t", "v"),  (1, "t", "h"),  (1, "t", "h"),  (1, "t", "h")],
                    [0,             0,              (2, "t", "v"),  (7, "c", "v"),  (8, "c", "h"),  (8, "c", "h")],
                    [0,             (3, "t", "v"),  (2, "t", "v"),  (7, "c", "v"),  0,              (0, "c", "v")],
                    [(4, "t", "v"), (3, "t", "v"),  (5, "t", "h"),  (5, "t", "h"),  (5, "t", "h"),  (0, "c", "v")],
                    [(4, "t", "v"), (3, "t", "v"),  0,              (6, "t", "h"),  (6, "t", "h"),  (6, "t", "h")],
                    [(4, "t", "v"), 0,              0,              0,              0,              0            ]]
n = 6
m = 6
goal = (0,5)

print(manhattan_heuristic.astar_search(n, m, initial_state, goal))

path, g = move_the_obstacle_heuristic.astar_search(n, m, initial_state, goal)
for state in path:
    move_the_obstacle_heuristic.print_traffic_jam(state)
print(g)"""