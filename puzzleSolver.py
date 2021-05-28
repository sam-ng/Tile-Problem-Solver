# Samuel Ng 112330868
# CSE 352 Assignment 1

from TileProblem import TileProblem
from Heuristics import Heuristics

# Python standard library
import sys
from queue import PriorityQueue
import math
import tracemalloc
import time

# takes in an input file and returns a matrix of ints representing the state of the board
def convert_txt_to_board(input_txt):
	inputLines = input_txt.read().splitlines()
	board = []
	for row in inputLines:
		lst = []
		nums = row.split(',')
		for num in nums:
			if num == '':
				lst.append(0)
			else:
				lst.append(int(num))
		board.append(lst)
	return board

# takes in a board and returns the position of the blank space (x, y)
def get_blank_pos(board):
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == 0:
				return (i, j)
	return (-1, -1)

# takes in the size of the puzzle and the position of the blank space and returns a list of the possible actions
def get_valid_actions(N, blank_pos):
	valid_actions = []
	if blank_pos[0] > 0:
		valid_actions.append('U')
	if blank_pos[1] < N-1:
		valid_actions.append('R')
	if blank_pos[0] < N-1:
		valid_actions.append('D')
	if blank_pos[1] > 0:
		valid_actions.append('L')
	return valid_actions

# performs A* graph search on a given problem and heuristic function, returns (# states explored, path to goal state) on success and False on failure
# modeled after class pseudocode
def A_star_graph_search(problem, N, H):
	frontier = PriorityQueue()
	explored = []
	g_cost = 0
	h_instance = Heuristics(H)
	h_instance.heuristic_cost(problem.state, problem.goal)
	h_cost = h_instance.h_cost
	f = g_cost + h_cost
	problem.f = f
	frontier.put((f, problem, g_cost, None, '')) # node consists of f value, tile problem, g value, parent node, and action from parent node

	while frontier:
		current_node = frontier.get()
		current = current_node[1] # current is a tile problem instance
		if current.is_solution():
			actions = []
			parent_node = current_node
			while parent_node is not None:
				action = parent_node[4]
				if action != '':
					actions.append(action)
				parent_node = parent_node[3]
			return (len(explored), actions)
		if current.state not in explored:
			explored.append(current.state)
			for action in current.actions:
				new_state = current.transition(action)
				blank_pos = get_blank_pos(new_state)
				actions = get_valid_actions(N, blank_pos)
				new = TileProblem(N, new_state, blank_pos, actions)

				g_cost = current_node[2] + 1
				h_instance.heuristic_cost(current.state, current.goal)
				h_cost = h_instance.h_cost
				f = g_cost + h_cost
				new.f = f
				frontier.put((f, new, g_cost, current_node, action))
	return False

# performs RBFS on a given problem and heuristic function, returns True on success and False on failure
rbfs_states = 0 # counter for keeping track of explored states for rbfs
def recursive_best_first_search(problem, N, H): # pseudocode from mtu.edu referenced
	g_cost = 0
	h_instance = Heuristics(H)
	h_instance.heuristic_cost(problem.state, problem.goal)
	h_cost = h_instance.h_cost
	f = g_cost + h_cost
	problem.f = f
	return RBFS([f, problem, g_cost, None, ''], math.inf, N, h_instance) # node consists of f value, tile problem, g value, parent node, and action from parent node

# recursive helper for RBFS
def RBFS(node, f_limit, N, h_instance):
	current = node[1]
	global rbfs_states
	rbfs_states += 1
	if current.is_solution():
		actions = []
		parent_node = node
		while parent_node is not None:
			action = parent_node[4]
			if action != '':
				actions.append(action)
			parent_node = parent_node[3]
		return (True, f_limit, actions) # returning (True for success, f_limit, solution path)
	successors = []
	for action in current.actions:
		new_state = current.transition(action)
		blank_pos = get_blank_pos(new_state)
		actions = get_valid_actions(N, blank_pos)
		new = TileProblem(N, new_state, blank_pos, actions)

		g_cost = node[2] + 1
		h_instance.heuristic_cost(current.state, current.goal)
		h_cost = h_instance.h_cost
		f = g_cost + h_cost
		new.f = f
		successors.append([f, new, g_cost, node, action])
	if not successors:
		return (False, math.inf, []) # if deadend, propagate infinity f value up path
	for successor in successors:
		successor[0] = max(successor[0], node[0]) # updating f with value from previous search if any
		successor[1].f = max(successor[0], node[0])
	while True:
		sorted_successors = sorted(successors, key=lambda successor: successor[0])
		best = sorted_successors[0] # successor with min f value
		if best[0] > f_limit: # none of the successors' f values are less than the f_limit
			return (False, best[0], []) # return (False, best f value, empty solution path)
		alternative = sorted_successors[1]
		result, best[0], actions = RBFS(best, min(f_limit, alternative[0]), N, h_instance) # the new f-limit is the minimum of the current f-limit and the f-value of the alternative path
		if result:
			return (result, best[0], actions)

# function for outputting solution to output text file, solution is a string in output format
def output(solution, outputPath):
	outF = open(outputPath, 'w')
	outF.write(solution)
	outF.close()

# main function for running the script
def main():
	A = int(sys.argv[1]) # algorithm
	N = int(sys.argv[2]) # N=3 for 8-puzzle, N=4 for 15-puzzle
	H = int(sys.argv[3]) # H=1 for h1, H=2 for h2
	inputPath = sys.argv[4]
	outputPath = sys.argv[5]
	inF = open(inputPath, 'r')
	board = convert_txt_to_board(inF)
	blank_pos = get_blank_pos(board)
	actions = get_valid_actions(N, blank_pos)
	problem = TileProblem(N, board, blank_pos, actions)
	
	time_start = time.time()
	tracemalloc.start()
	if A == 1:
		searchReturn = A_star_graph_search(problem, N, H) # returns a tuple with the number of states and path to goal in reverse
	elif A == 2:
		searchReturn = recursive_best_first_search(problem, N, H)
	else:
		print('Invalid A.')
	current, peak = tracemalloc.get_traced_memory()
	time_end = time.time()
	tracemalloc.stop()
	if searchReturn:
		# solution was found
		print('Success')
		print(f"Current memory usage is {current / 10**6} MB; Peak was {peak / 10**6} MB")
		print(f"Time: {(time_end - time_start) * 1000} ms")
		if A == 1:
			states = searchReturn[0]
			path = searchReturn[1]
		elif A == 2:
			path = searchReturn[2]
		path.reverse()
		path_str = ','.join(path)
		if A == 1:
			print(f'States explored: {states}')
		elif A == 2:
			print(f'States explored: {rbfs_states}')
		print(f'Path: {path_str}')
		print(f'Depth: {len(path_str) - path_str.count(",")}')
		output(path_str, outputPath)
	else:
		print('Failure')
	inF.close()

if __name__ == '__main__':
	main()