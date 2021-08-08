#------------------------------------------------------
# Name: Path Finder A*
# Author: Laura Homet Garcia
# Date: May 11 2021
#------------------------------------------------------
import pygame
import math
from queue import PriorityQueue
import constants as C

WIN = pygame.display.set_mode((C.GRID["width"],C.GRID["width"]))
pygame.display.set_caption("A* Path Finding Algorithm")

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = C.RGB["empty"]
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

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

	def update_neighbors(self, grid):
		self.neighbors = []

		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])


	def __lt__(self, other):
		return False

def h(p1, p2):
	# Manhattan distance
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, start, current, draw):
	while current in came_from:
		current = came_from[current]
		if current != start:
			current.make_path()
			draw()

def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))

	came_from = {}

	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0

	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2] # Get node only
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, start, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1 # 1 node over

			if temp_g_score < g_score[neighbor]:
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				came_from[neighbor] = current

				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows

	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid

def draw_grid(win, rows, width):
	gap = width // rows

	for i in range(rows):
		pygame.draw.line(win, C.RGB["line"], (0, i * gap), (width, i * gap))

	for j in range(rows):
		pygame.draw.line(win, C.RGB["line"], (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
	win.fill(C.RGB["empty"])

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def main(win, width):
	grid = make_grid(C.GRID["rows"], width)

	start = None
	end = None

	run = True
	started = False

	while run:

		for event in pygame.event.get():
			draw(win, grid, C.GRID["rows"], width)

			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # clicked left button
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, C.GRID["rows"], width)
				spot = grid[row][col]

				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # clicked right button
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, C.GRID["rows"], width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, C.GRID["rows"], width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(C.GRID["rows"], width)

	pygame.quit()

main(WIN, C.GRID["width"])



