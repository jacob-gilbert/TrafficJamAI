import traffic_jam
import manhattan_heuristic
import move_the_obstacle_heuristic
import line_heuristic
import time

initial_state = [   [0,             0,              0,              0,              0               ],
                    [(1, "c", "h"), (1, "c", "h"),   0,             0,              0               ],
                    [(2, "c", "v"), 0,              0,              (3, "c", "h"),  (3, "c", "h")   ],
                    [(2, "c", "v"), (4, "c", "h"), (4, "c", "h"),  0,              (0, "c", "v")   ],
                    [(5, "t", "h"), (5, "t", "h"),  (5, "t", "h"),  0,              (0, "c", "v")   ]
                ]

n = 5
m = 5      
goal = (0,4)          
"""print("Test1")
#print(manhattan_heuristic.astar_search(n, m, initial_state, goal))
#print(traffic_jam.astar_search(n, m, initial_state, goal))
path, g = move_the_obstacle_heuristic.astar_search(n, m, initial_state, goal)
print(g)
print(line_heuristic.astar_search(n, m, initial_state, goal))
print()"""


initial_state = [   [0,              0,              0               ],
                    [0,              0,              0               ],
                    [0,              (3, "c", "h"),  (3, "c", "h")   ],
                    [(4, "c", "v"),  0,              (0, "c", "v")   ],
                    [(4, "t", "v"),  0,              (0, "c", "v")   ]
                ]

n = 5
m = 3      
goal = (0,2)          
"""print("Test2")
print(manhattan_heuristic.astar_search(n, m, initial_state, goal))
print(traffic_jam.astar_search(n, m, initial_state, goal))
path, g = move_the_obstacle_heuristic.astar_search(n, m, initial_state, goal)
print(g)
print(line_heuristic.astar_search(n, m, initial_state, goal))
print()"""


initial_state = [   [0,  (3, "c", "h"),  (3, "c", "h")   ],
                    [(4, "c", "v"),  0,              (0, "c", "v")   ],
                    [(4, "c", "v"),  0,              (0, "c", "v")   ]
                ]

n = 3
m = 3      
goal = (0,2) 
"""print("Test3")
print(manhattan_heuristic.astar_search(n, m, initial_state, goal))
print(traffic_jam.astar_search(n, m, initial_state, goal))
path, g = move_the_obstacle_heuristic.astar_search(n, m, initial_state, goal)
print(g)
print(line_heuristic.astar_search(n, m, initial_state, goal))
print()"""



initial_state = [   [0,             0,              0,              (1, "t", "h"),  (1,"t","h"),    (1,"t","h")    ],
                    [0,             0,              (2, "c", "v"),  0,              (0, "c", "v"),  0              ],
                    [0,             0,              (2, "c", "v"),  0,              (0, "c", "v"),  0              ],
                    [0,             0,              0,              0,               0,             0              ]
                ]

n = 4
m = 6  
goal = (0, 4)      
        
"""print("Test4")
print(manhattan_heuristic.astar_search(n, m, initial_state, goal))
print(traffic_jam.astar_search(n, m, initial_state, goal))
path, g = move_the_obstacle_heuristic.astar_search(n, m, initial_state, goal)
print(g)
print(line_heuristic.astar_search(n, m, initial_state, goal))
print()"""


initial_state = [   [0,             0,              (3, "c", "h"),  (3, "c", "h"),  (1, "c", "h"),  (1, "c", "h")  ],
                    [0,             0,              0,              0,              (0, "c", "v"),  0              ],
                    [0,             0,              0,              0,              (0, "c", "v"),  0              ]
                ]

n = 3
m = 6                
goal = (0,4)

"""print("Test5")
print(manhattan_heuristic.astar_search(n, m, initial_state, goal))
print(traffic_jam.astar_search(n, m, initial_state, goal))
path, g = move_the_obstacle_heuristic.astar_search(n, m, initial_state, goal)
print(g)
print(line_heuristic.astar_search(n, m, initial_state, goal))
print()"""


initial_state = [   [0,             0,              (3, "c", "h"),  (3, "c", "h"),  (1, "c", "h"),  (1, "c", "h")  ],
                    [0,             0,              (2, "c", "v"),  0,              (0, "c", "v"),  0              ],
                    [0,             0,              (2, "c", "v"),  0,              (0, "c", "v"),  0              ],
                    [0,             0,              0,              0,               0,             0              ]
                ]

n = 4
m = 6                
goal = (0,4)

#print("Test6")
#print(manhattan_heuristic.astar_search(n, m, initial_state, goal))
#print(traffic_jam.astar_search(n, m, initial_state, goal))
#path, g = move_the_obstacle_heuristic.astar_search(n, m, initial_state, goal)
#print(g)
#for state in path:
#    move_the_obstacle_heuristic.print_traffic_jam(state)
#    print("\n")
#print(line_heuristic.astar_search(n, m, initial_state, goal))
#print("\n")


initial_state = [   [0,             0,              0,              (8, "t", "h"),  (8, "t", "h"),      (8, "t", "h")],
                    [(1, "c", "h"), (1, "c", "h"),  0,              (2, "c", "h"),  (2, "c", "h"),      0],
                    [(2, "c", "v"), (7, "c", "h"),  (7, "c", "h"),  0,              (0, "c", "v"),      0],
                    [(2, "c", "v"), (4, "c", "h"),  (4, "c", "h"),  0,              (0, "c", "v"),      0],
                    [(5, "t", "h"), (5, "t", "h"),  (5, "t", "h"),  0,              0,                  0 ]]
n = 5
m = 6
goal = (0,4)

"""print("Test7")
#print(manhattan_heuristic.astar_search(n, m, initial_state, goal))
#print(traffic_jam.astar_search(n, m, initial_state, goal))
path, g = move_the_obstacle_heuristic.astar_search(n, m, initial_state, goal)
print(g)
print(line_heuristic.astar_search(n, m, initial_state, goal))
print()"""


initial_state = [   [0,             0,              (2, "t", "v"),  (1, "t", "h"),  (1, "t", "h"),  (1, "t", "h")],
                    [0,             0,              (2, "t", "v"),  (7, "c", "v"),  (8, "c", "h"),  (8, "c", "h")],
                    [0,             0,              (2, "t", "v"),  (7, "c", "v"),  0,              (0, "c", "v")],
                    [0,             0,              (5, "t", "h"),  (5, "t", "h"),  (5, "t", "h"),  (0, "c", "v")],
                    [0,             0,              0,              (6, "t", "h"),  (6, "t", "h"),  (6, "t", "h")],
                    [0,             0,              0,              0,              0,              0            ]]
#print("Test8")
n = 6
m = 6
goal = (0, 5)
#path, g = move_the_obstacle_heuristic.astar_search(n, m, initial_state, goal)
#print(g)
#print(line_heuristic.astar_search(n, m, initial_state, goal)) # passes



initial_state = [   [0,             0,              0,              (4, "c", "v"),  (5, "c", "h"),  (5, "c", "h")],
                    [0,             0,              0,              (4, "c", "v"),  (2, "c", "h"),  (2, "c", "h")],
                    [(1, "c", "v"), (7, "t", "h"),  (7, "t", "h"),  (7, "t", "h"),  (3, "c", "h"),  (3, "c", "h")],
                    [(1, "c", "v"), 0,              0,              0,              0,              (0, "c", "v")],
                    [0,             0,              (6, "t", "h"),  (6, "t", "h"),  (6, "t", "h"),  (0, "c", "v")],
                    [0,             0,              0,              0,              0,              0            ]]
n = 6
m = 6
goal = (0,5)

"""print("Park Test1")
start_time = time.time()
print(manhattan_heuristic.astar_search(n, m, initial_state, goal))
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")"""

"""start_time = time.time()
print(traffic_jam.astar_search(n, m, initial_state, goal))
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")"""

start_time = time.time()
path, g = move_the_obstacle_heuristic.astar_search(n, m, initial_state, goal)
print(g)
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

start_time = time.time()
path, g = line_heuristic.astar_search(n, m, initial_state, goal)
print(g)
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

#for state in path:
#    move_the_obstacle_heuristic.print_traffic_jam(state)
#    print("\n")
print()



initial_state = [   [(1, "t", "v"), (2, "t", "v"),  (6, "c", "v"),  (3, "t", "h"),  (3, "t", "h"),  (3, "t", "h")],
                    [(1, "t", "v"), (2, "t", "v"),  (6, "c", "v"),  (4, "t", "h"),  (4, "t", "h"),  (4, "t", "h")],
                    [(1, "t", "v"), (2, "t", "v"),  (7, "c", "h"),  (7, "c", "h"),  (9, "c", "h"),  (9, "c", "h")],
                    [(5, "c", "h"), (5, "c", "h"),  0,              0,              (0, "c", "v"),  0            ],
                    [0,             0,              0,              0,              (0, "c", "v"),  0            ],
                    [0,             0,              (8, "c", "h"),  (8, "c", "h"),  0,              0            ]]
n = 6
m = 6
goal = (0,4)

"""print("Park Test2")
start_time = time.time()
print(manhattan_heuristic.astar_search(n, m, initial_state, goal))
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")"""

"""start_time = time.time()
print(traffic_jam.astar_search(n, m, initial_state, goal))
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")"""

start_time = time.time()
path, g = move_the_obstacle_heuristic.astar_search(n, m, initial_state, goal)
print(g)
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
print()

start_time = time.time()
path, g = line_heuristic.astar_search(n, m, initial_state, goal)
print(g)
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
print()



initial_state = [   [0,             0,              (2, "t", "v"),  (1, "t", "h"),  (1, "t", "h"),  (1, "t", "h")],
                    [0,             0,              (2, "t", "v"),  (7, "c", "v"),  (8, "c", "h"),  (8, "c", "h")],
                    [0,             (3, "t", "v"),  (2, "t", "v"),  (7, "c", "v"),  0,              (0, "c", "v")],
                    [(4, "t", "v"), (3, "t", "v"),  (5, "t", "h"),  (5, "t", "h"),  (5, "t", "h"),  (0, "c", "v")],
                    [(4, "t", "v"), (3, "t", "v"),  0,              (6, "t", "h"),  (6, "t", "h"),  (6, "t", "h")],
                    [(4, "t", "v"), 0,              0,              0,              0,              0            ]]
n = 6
m = 6
goal = (0,5)

"""print("Park Test3")
start_time = time.time()
print(manhattan_heuristic.astar_search(n, m, initial_state, goal))
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")"""

"""start_time = time.time()
print(traffic_jam.astar_search(n, m, initial_state, goal))
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")"""

start_time = time.time()
path, g = move_the_obstacle_heuristic.astar_search(n, m, initial_state, goal)
print(g)
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

start_time = time.time()
path, g = line_heuristic.astar_search(n, m, initial_state, goal)
print(g)
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
print("\n")