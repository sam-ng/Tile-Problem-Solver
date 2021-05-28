# Samuel Ng 112330868
# CSE 352 Assignment 1

# imported copy for deep copying lists
import copy

class TileProblem:

	# TileProblem constructor
	def __init__(self, N, board, blank_pos, actions):
		self.state = board
		self.blank_pos = blank_pos # position of blank tile
		self.actions = actions
		self.f = 0 # f value of TileProblem
		# goal states are known
		if N == 3:
			self.goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
		elif N == 4:
			self.goal = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
		else:
			print('Invalid puzzle size.')

	# transition function for taking current state and action and returning the new state
	def transition(self, action):
		i = self.blank_pos[0]
		j = self.blank_pos[1]
		new_state = copy.deepcopy(self.state)
		if (action == 'U'):
			new_state[i][j], new_state[i-1][j] = new_state[i-1][j], new_state[i][j]
		elif (action == 'R'):
			new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]
		elif (action == 'D'):
			new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
		elif (action == 'L'):
			new_state[i][j], new_state[i][j-1] = new_state[i][j-1], new_state[i][j]
		else:
			print('Invalid action.')
		return new_state

	# goal test method
	def is_solution(self):
		return self.state == self.goal

	# for priority queue comparator to work when f values are equal
	def __lt__(self, other):
		return self.f < other.f