import sys
from queue import PriorityQueue
import board
import timer

@timer.stopwatch
def depth_first(initial_state):
	open_l = [("0", board.Board(initial_state))]
	closed_l = []
	
	while(open_l):
		x = open_l.pop()
		if x[1].goal_reached(): 
			solution = x[1].parents
			solution.append((x[0], x[1].state))
			return solution
		else:
			closed_l.append(x[1].state)
			new_moves = x[1].get_children(x[0]) ## Generate all possible moves from x, ordered by hierarchy
			for move in new_moves:
				open_l_states = [i[1].state for i in open_l]
				if move[1].state not in open_l_states and move[1].state not in closed_l:
					open_l.append(move) ## If children are not already in open or closed, append to open
	return []

@timer.stopwatch
def best_first(initial_state, h_func):
	open_l = PriorityQueue()
	open_l.put((h_func(initial_state), ("0", board.Board(initial_state))))
	closed_l = []
	
	while not open_l.empty():
		x = open_l.get()[1]
		if x[1].goal_reached():
			solution = x[1].parents
			solution.append((x[0], x[1].state))
			return solution
		else:
			closed_l.append(x[1].state)
			new_moves = x[1].get_children(x[0])
			for move in new_moves:
				if move[1].state not in open_l.queue and move[1].state not in closed_l:
					open_l.put((h_func(move[1].state), move))
	return []

@timer.stopwatch
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
			return solution
		else:
			closed_l.append(x[1].state)
			new_moves = x[1].get_children(x[0])
			for move in new_moves:
				if move[1].state not in open_l.queue and move[1].state not in closed_l:
					open_l.put((f_func(h_func, move[1]), move))
	return []

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

            	if a[0] != b[0]:
            		score += 1
            	if a[1] != b[1]:
            		score += 1
	return score

def f_func(h_func, board):
	return h_func(board.state) + g_func(board)

def g_func(board):
	return board.num_of_parents

def test():
    testBoard = board.Board([[1,2,3,4],[5,6,7,8],[9,10,11,0]])
    print(testBoard)
    
    next_moves = testBoard.get_moves()
    print(next_moves)
    
    children = testBoard.get_children()
    for child in children:
        print(child[0])
        print(child[1])
        print(child[1].get_children())


raw_state = sys.argv[1:]

for i in raw_state:
	raw_state[raw_state.index(i)] = int(i)

initial_state = [raw_state[0:4], raw_state[4:8], raw_state[8:12]]
#initial_state = [[1,2,3,4],[5,6,8,7],[9,10,0,11]]
# initial_state = [[1, 0, 3, 7], [5, 2, 6, 4], [9, 10, 11, 8]] 
# result = depth_first(initial_state)
result = best_first(initial_state, manh_dist)
# result = a_star(initial_state, manh_dist)
print(result)
print(len(result))
