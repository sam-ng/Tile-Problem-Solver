# Samuel Ng 112330868
# CSE 352 Assignment 1

class Heuristics:

	def __init__(self, H):
		self.H = H
		self.h_cost = 0

	# function wrapper that chooses one of the heuristic functions based on H
	def heuristic_cost(self, state, goal):
		if self.H == 1:
			self.h_cost = self.heuristic1(state, goal)
		elif self.H == 2:
			self.h_cost = self.heuristic2(state, goal)
		else:
			print('Invalid heuristic.')

	# return the number of misplaced tiles
	def heuristic1(self, state, goal):
		count = 0
		for i in range(len(state)):
			for j in range(len(state[i])):
				if state[i][j] == 0: # don't count blank tile
					continue
				if state[i][j] != goal[i][j]:
					count += 1
		return count

	# return the sum of manhattan distances of each numbered tile to its goal position
	def heuristic2(self, state, goal):
		manhattan_sum = 0
		for i in range(len(state)):
			for j in range(len(state[i])):
				if state[i][j] == 0: # don't count blank tile
					continue
				if state[i][j] != goal[i][j]:
					goal_row = (state[i][j]-1) // len(state)
					goal_col = (state[i][j]-1) % len(state)
					manhattan_sum += abs(goal_col - j) + abs(goal_row - i)
		return manhattan_sum
