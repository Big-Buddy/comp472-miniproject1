import sys
from queue import PriorityQueue
import board
import timer
import itertools

#@timer.stopwatch
def depth_first(initial_state):
	open_l = [("0", board.Board(initial_state))]
	closed_l = []
	
	while open_l:
		x = open_l.pop()
		if x[1].goal_reached(): 
			solution = x[1].parents
			solution.append((x[0], x[1].state))
			return (solution, len(closed_l))
		else:
			if len(closed_l) >= 1:
				break
			closed_l.append(x[1].state)
			new_moves = x[1].get_children(x[0]) ## Generate all possible moves from x, ordered by hierarchy
			for move in new_moves:
				open_l_states = [i[1].state for i in open_l]
				if move[1].state not in open_l_states and move[1].state not in closed_l:
					open_l.append(move) ## If children are not already in open or closed, append to open
	return ([], len(closed_l))

#@timer.stopwatch
def best_first(initial_state, h_func):
	open_l = PriorityQueue()
	open_l.put((h_func(initial_state), ("0", board.Board(initial_state))))
	closed_l = []
	
	while not open_l.empty():
		x = open_l.get()[1]
		if x[1].goal_reached():
			solution = x[1].parents
			solution.append((x[0], x[1].state))
			return (solution, len(closed_l))
		else:
			if len(closed_l) >= 1000:
				break
			closed_l.append(x[1].state)
			new_moves = x[1].get_children(x[0])
			for move in new_moves:
				if move[1].state not in open_l.queue and move[1].state not in closed_l:
					open_l.put((h_func(move[1].state), move))
	return ([], len(closed_l))

#@timer.stopwatch
def a_star(initial_state, h_func):
	start = board.Board(initial_state)
	open_l = PriorityQueue()
	open_l.put((f_func(h_func, start), ("0", start)))
	closed_l = []

	while not open_l.empty():
		x = open_l.get()[1]
		if x[1].goal_reached():
			solution = x[1].parents
			solution.append((x[0], x[1].state))
			return (solution, len(closed_l))
		else:
			if len(closed_l) >= 1000:
				break
			closed_l.append(x[1].state)
			new_moves = x[1].get_children(x[0])
			for move in new_moves:
				if move[1].state not in open_l.queue and move[1].state not in closed_l:
					open_l.put((f_func(h_func, move[1]), move))
	return ([], len(closed_l))

def manh_dist(state):
	"""
	First heuristic function, computes the Manhattan distance in terms of the array indices as x-y coordinates
	"""

	score = 0
	goal_states = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 0]]
	goal_coord = dict( (j,(x, y)) for x, i in enumerate(goal_states) for y, j in enumerate(i) )

	for row_num, row in enumerate(state):
		for col_num, tile in enumerate(row):
			if tile != 0:
				a = (row_num, col_num)
				b = goal_coord[tile]
				score += max(abs(a[0]-b[0]), abs(a[1]-b[1]))
	return score

def row_col_diff(state):
	"""
	Second heuristic function, computes the number of tiles out of row plus the number of tiles out of column
	"""

	score = 0
	goal_states = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 0]]
	goal_coord = dict( (j,(x, y)) for x, i in enumerate(goal_states) for y, j in enumerate(i) )

	for row_num, row in enumerate(state):
            for col_num, tile in enumerate(row):
            	a = (row_num, col_num)
            	b = goal_coord[tile]

            	if a[0] != b[0] | a[1] != b[1]:
            		score += 1
	return score

def f_func(h_func, board):
	return h_func(board.state) + g_func(board)

def g_func(board):
	return len(board.parents)

@timer.stopwatch
def run_experiment(search_alg, h_func=None):
	test_cases = [[[1, 0, 3, 7], [5, 2, 6, 4], [9, 10, 11, 8]],
				  [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 0, 11]],
				  [[1, 2, 3, 4], [5, 6, 7, 0], [9, 10, 11, 8]],
				  [[0, 11, 10, 9], [8, 7, 6, 5], [4, 3, 2, 1]],
				  [[5, 6, 7, 8], [1, 2, 3, 4], [9, 10, 11, 0]],
				  [[9, 10, 11, 0], [5, 6, 7, 8], [1, 2, 3, 4]],
				  [[2, 4, 3, 1], [11, 7, 6, 0], [8, 5, 10, 9]],
				  [[11, 1, 5, 9], [10, 2, 7, 4], [8, 3, 6, 0]],
				  [[2, 5, 6, 7], [1, 3, 4, 8], [0, 10, 9, 11]],
				  [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]]]
	avg_exp_buffer = 0
	avg_solution_buffer = 0
	num_of_success = 0

	if h_func != None:
		for i in test_cases:
			result = search_alg(i, h_func)
			if result[0]:
				num_of_success += 1
			avg_exp_buffer += result[1]
			avg_solution_buffer += len(result[0])
			print("Number of nodes expanded: " + str(result[1]))
			print("Solution path length: " + str(len(result[0])))
	else:
		for i in test_cases:
			result = search_alg(i)
			if result[0]:
				num_of_success += 1
			avg_exp_buffer += result[1]
			avg_solution_buffer += len(result[0])
			print("Number of nodes expanded: " + str(result[1]))
			print("Solution path length: " + str(len(result[0])))

	print("Average number of nodes expanded: " + str(avg_exp_buffer/10))
	if num_of_success > 0:
		print("Average solution path length: " + str(avg_solution_buffer/num_of_success))

def driver():
	print("*********************************")
	print("*********************************")
	run_experiment(depth_first)
	print("*********************************")
	print("*********************************")
	run_experiment(best_first, manh_dist)
	print("*********************************")
	print("*********************************")
	run_experiment(best_first, row_col_diff)
	print("*********************************")
	print("*********************************")
	run_experiment(a_star, manh_dist)
	print("*********************************")
	print("*********************************")
	run_experiment(a_star, row_col_diff)
	print("*********************************")
	print("*********************************")

def write_to_file(filename, solution):
	f = open(filename, "w")
	flat_solution = list(itertools.chain(*solution))
	for i in flat_solution:
		f.write("%s\n" % i)

raw_state = sys.argv[1:]

for i in raw_state:
	raw_state[raw_state.index(i)] = int(i)

initial_state = [raw_state[0:4], raw_state[4:8], raw_state[8:12]]
#initial_state = [[1,2,3,4],[5,6,8,7],[9,10,0,11]]
#initial_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 11, 10, 0]]

if raw_state:
	"""
	Split the raw input into an initial state and run all possible experiments, write the result to a file
	"""
	initial_state = [raw_state[0:4], raw_state[4:8], raw_state[8:12]]
	#Best-first search - manhattan distance
	result_bfs_h1 = best_first(initial_state, manh_dist)
	for i in result_bfs_h1[0]: print(i)
	print("Length of BFS solution path using h1: {}".format(len(result_bfs_h1[0])))

	#Best-first search - row column difference
	result_bfs_h2 = best_first(initial_state, row_col_diff)
	for i in result_bfs_h2[0]: print(i)
	print("Length of BFS solution path using h2: {}".format(len(result_bfs_h2[0])))

	#A* - manhattan distance
	result_a_h1 = a_star(initial_state, manh_dist)
	for i in result_a_h1[0]: print(i)
	print("Length of A* solution path using h1: {}".format(len(result_a_h1[0])))

	#A* - row column difference
	result_a_h2 = a_star(initial_state, row_col_diff)
	for i in result_a_h2[0]: print(i)
	print("Length of A* solution path using h2: {}".format(len(result_a_h2[0])))

	write_to_file("puzzleBFS-h1.txt", result_bfs_h1[0])
	write_to_file("puzzleBFS-h2.txt", result_bfs_h2[0])
	write_to_file("puzzleAs-h1.txt", result_a_h1[0])
	write_to_file("puzzleAs-h2.txt", result_a_h2[0])
else:
	"""
	Run all possible experiments with 10 preset initial states
	"""
	driver()