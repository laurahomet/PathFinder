#------------------------------------------------------
# Name: Path Finder A* Model
# Author: Laura Homet Garcia
# Date: May 11 2021
#------------------------------------------------------
import constants as C
from queue import PriorityQueue
from datetime import datetime
import csv

class Spot:
	def __init__(self, row, col):
		self.row = row
		self.col = col
		self.x = row * C.SPOT_SZ
		self.y = col * C.SPOT_SZ
		self.color = C.RGB["empty"]
		self.neighbors = []

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == C.RGB["closed"]

	def is_open(self):
		return self.color == C.RGB["open"]

	def is_barrier(self):
		return self.color == C.RGB["barrier"]

	def is_start(self):
		return self.color == C.RGB["start"]

	def is_end(self):
		return self.color == C.RGB["end"]

	def reset(self):
		self.color = C.RGB["empty"]

	def make_start(self):
		self.color = C.RGB["start"]

	def make_closed(self):
		self.color = C.RGB["closed"]

	def make_open(self):
		self.color = C.RGB["open"]

	def make_barrier(self):
		self.color = C.RGB["barrier"]

	def make_start(self):
		self.color = C.RGB["start"]

	def make_end(self):
		self.color = C.RGB["end"]

	def make_path(self):
		self.color = C.RGB["path"]

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, spots):
		self.neighbors = []

		if self.row < C.GRID["rows"] - 1 and not spots[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(spots[self.row + 1][self.col])

		if self.row > 0 and not spots[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(spots[self.row - 1][self.col])

		if self.col < C.GRID["rows"] - 1 and not spots[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(spots[self.row][self.col + 1])

		if self.col > 0 and not spots[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(spots[self.row][self.col - 1])


class Model(object):

	def __init__(self, controller):
		self.controller = controller
		self.make_spots()

	def save_map(self, text):

		spots_map = []

		for i in range(C.GRID["rows"]):
			spots_map.append([])
			for j in range(C.GRID["rows"]):
				spots_map[i].append(C.MAP["empty"])

		for i,row in enumerate(self.spots):
			for j,spot in enumerate(row):
				if spot.is_start():
					spots_map[j][i]=C.MAP["start"]
				elif spot.is_end():
					spots_map[j][i]=C.MAP["end"]
				elif spot.is_barrier():
					spots_map[j][i]=C.MAP["barrier"]

		with open(text, 'w') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			for line in spots_map:
				writer.writerow(line)

	def load_map(self, text):
		with open(text, 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for i,line in enumerate(reader):
				for j,value in enumerate(line):
					if value == str(C.MAP["start"]):
						self.start = self.spots[j][i]
						self.start.make_start()
					elif value == str(C.MAP["end"]):
						self.end = self.spots[j][i]
						self.end.make_end()
					elif value == str(C.MAP["barrier"]):
						self.spots[j][i].make_barrier()

	def make_spots(self):
		self.spots = []
		self.start = None
		self.end = None

		for i in range(C.GRID["rows"]):
			self.spots.append([])

			for j in range(C.GRID["rows"]):
				spot = Spot(i, j)
				self.spots[i].append(spot)

	def get_spot(self, row, col):
		return self.spots[row][col]

	def get_spots(self):
		return self.spots

	def reset_spot(self, row, col):
		self.spots[row][col].reset()

	def create_barrier(self, row, col):
		self.spots[row][col].make_barrier()

	def update_neighbors(self):
		for row in self.spots:
			for spot in row:
				spot.update_neighbors(self.spots)

	def start_timer(self):
		self.start_time = datetime.now()

	def stop_timer(self):
		self.stop_time = datetime.now()

	def _h(self, p1, p2):
		# Manhattan distance
		x1, y1 = p1
		x2, y2 = p2
		return abs(x1 - x2) + abs(y1 - y2)

	def run_algorithm(self):

		count = 0
		open_set = PriorityQueue() # Doesn't support removing items by name
		open_set.put((0, count, self.start))

		came_from = {}

		g = {spot: float("inf") for row in self.spots for spot in row}
		g[self.start] = 0
		f = {}

		open_set_hash = {self.start}

		while not open_set.empty():

			current = open_set.get()[2] # Get spot with best f score
			open_set_hash.remove(current)

			if current == self.end:
				self._reconstruct_path(current, came_from)
				self.end.make_end()
				return True

			for neighbor in current.neighbors:
				temp_g = g[current] + 1 # 1 spot over

				if temp_g < g[neighbor]:
					g[neighbor] = temp_g
					f[neighbor] = temp_g + self._h(neighbor.get_pos(), self.end.get_pos())
					came_from[neighbor] = current

					if neighbor not in open_set_hash:
						count += 1
						open_set.put((f[neighbor], count, neighbor))
						open_set_hash.add(neighbor)
						if neighbor != self.end:
							neighbor.make_open()

			self.controller.refresh_spots(self.spots)

			if current != self.start:
				current.make_closed()

		return False

	def _reconstruct_path(self, current, came_from):

		while current in came_from:
			current = came_from[current]
			if current != self.start and current != self.end:
				current.make_path()
				self.controller.refresh_spots(self.spots)

