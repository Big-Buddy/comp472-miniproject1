import sys
from queue import PriorityQueue

def depth_first(initial_state):
	open_l = [initial_state]
	closed_l = []
	move_buffer = [(0, initial_state)]
	
	while(open_l):
		x = open_l.pop()
		move_buffer.append((x.letter, x.state))
		if check_goal(x): 
			return move_buffer
		else:
			closed_l.append(x)
			new_moves = generate_children(x) ## Generate all possible moves from x, ordered by hierarchy
			for move in new_moves:
				if move[1] not in open_l or move[1] not in closed_l:
					open_l.append(move) ## If children are not already in open or closed, append to open
	return []

def best_first(initial_state, h_func):
	open_l = PriorityQueue().put((h_func(initial_state), initial_state))
	closed_l = []
	move_buffer = [(0, initial_state)]
	
	while not open_l.empty():
		x = open_l.get()[1]
		move_buffer.append(x.letter, x.state)
		if check_goal(x):
			return move_buffer
		else:
			closed_l.append(x)
			new moves = generate_children(x)

			for move in new_moves:
				if move[1] not in open_l.queue and move[1] not in closed_l:
					open_l.put((h_func(move), move))
	return []

def a_star(initial_state, h_func):
	open_l = PriorityQueue().put((f_func(h_func, initial_state), initial_state))
	closed_l = []
	move_buffer = [(0, initial_state)]

	while not open_l.empty():
		x = open_l.get()[1]
		move_buffer.append(x.letter, x.state)
		if check_goal(x):
			return move_buffer
		else:
			closed_l.append(x)
			new_moves = generate_children(x)
			
			for move in new_moves:
				if move[1] not in open_l.queue and move[1] not in closed_l:
					open_l.put((f_func(move), move))
	return []
		

raw_state = sys.argv[1:]

for i in raw_state:
	raw_state[raw_state.index(i)] = int(i)

initial_state = [raw_state[0:4], raw_state[4:8], raw_state[8:12]]


