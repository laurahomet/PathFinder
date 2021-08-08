#------------------------------------------------------
# Name: Path Finder A* View
# Author: Laura Homet Garcia
# Date: May 11 2021
#------------------------------------------------------
import pygame
import model as m
import constants as C

class View():

	def __init__(self, controller):
		self.controller = controller
		self._setup_window()
		self._init_display()
		self._init_text_box()
		self.text = ''
		self.reading = None
		self.run = True

	def _setup_window(self):
		self.window = pygame.display.set_mode((C.GRID["width"],C.GRID["width"]))
		pygame.display.set_caption("A* Path Finding Algorithm")

	def _init_display(self):
		self.window.fill(C.RGB["empty"])
		self._draw_grid()
		pygame.display.update()

	def _init_text_box(self):
		pygame.font.init()
		self.text_color = C.BLACK
		self.text_font = pygame.font.Font(None,32)
		self.box_rect = pygame.Rect(15,15,200,30)
		self.box_color = pygame.Color('gray')

	def _draw_grid(self):
		for i in range(C.GRID["rows"]):
			pygame.draw.line(self.window, C.RGB["line"], (0, i * C.SPOT_SZ), (C.GRID["width"], i * C.SPOT_SZ))

		for j in range(C.GRID["rows"]):
			pygame.draw.line(self.window, C.RGB["line"], (j * C.SPOT_SZ, 0), (j * C.SPOT_SZ, C.GRID["width"]))

	def _draw_spots(self, spots):
		for row in spots:
			for spot in row:
				pygame.draw.rect(self.window, spot.color, (spot.x, spot.y, C.SPOT_SZ, C.SPOT_SZ))

	def _draw_box(self):
		pygame.draw.rect(self.window, self.box_color, self.box_rect)

		surface = self.text_font.render(self.text,True,self.text_color)
		self.window.blit(surface,(20,20))

	def refresh_display(self, spots):
		self.window.fill(C.RGB["empty"])
		self._draw_spots(spots)
		self._draw_grid()

		if self.reading != None:
			self._draw_box()

		pygame.display.update()

	def _get_spot_pos(self, pos):
		y, x = pos

		row = y // C.SPOT_SZ
		col = x // C.SPOT_SZ

		return row, col

	def quit(self):
		self.run = False

	def mainloop(self):

		while self.run:
			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					self.controller.pressed_quit()

				if event.type == pygame.KEYDOWN:

					if self.reading:

						if event.key == pygame.K_RETURN:
							self.controller.pressed_enter()
						else:
							self.controller.pressed_char(event.unicode)

					else:
						if event.key == pygame.K_SPACE:
							self.controller.pressed_space()

						if event.key == pygame.K_s:
							self.controller.pressed_S()

						if event.key == pygame.K_l:
							self.controller.pressed_L()

						if event.key == pygame.K_c:
							self.controller.pressed_C()

				if pygame.mouse.get_pressed()[0]: # clicked left button
					spot_pos = self._get_spot_pos(pygame.mouse.get_pos())
					self.controller.clicked_left(spot_pos)

				elif pygame.mouse.get_pressed()[2]: # clicked right button
					spot_pos = self._get_spot_pos(pygame.mouse.get_pos())
					self.controller.clicked_right(spot_pos)

		pygame.quit()
