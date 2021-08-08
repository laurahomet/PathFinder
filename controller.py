#------------------------------------------------------
# Name: Path Finder A* Controller
# Author: Laura Homet Garcia
# Date: May 11 2021
#------------------------------------------------------
import model as m
import view as v

class Controller(object):
	
	def __init__(self):
		self.model = m.Model(self)
		self.view = v.View(self)
		self.run = True

	def pressed_quit(self):
		self.view.quit()

	def pressed_space(self):

		if self.model.start and self.model.end:
			self.model.update_neighbors()
			self.model.start_timer()

			if self.model.run_algorithm():
				print("Found path! ", end ="Time: ")
			else:
				print("Couldn't find path... ", end ="Time: ")

			self.model.stop_timer()
			print(self.model.stop_time - self.model.start_time)

	def pressed_S(self):
		self.view.reading = 'saving'
		self._refresh()

	def pressed_L(self):
		self.view.reading = 'loading'
		self._refresh()

	def pressed_char(self, char):
		self.view.text += char
		self._refresh()

	def pressed_enter(self):

		if self.view.reading == 'saving':
			self.model.save_map(self.view.text)

		elif self.view.reading == 'loading':
			self.model.make_spots()
			self.model.load_map(self.view.text)

		self.view.reading = None
		self.view.text = ''
		self._refresh()

	def pressed_C(self):
		self.model.make_spots()
		self._refresh()

	def clicked_left(self, pos):
		row, col = pos
		spot = self.model.get_spot(row,col)

		if not self.model.start and spot != self.model.end:
			self.model.start = spot
			self.model.start.make_start()
			self._refresh()

		elif not self.model.end and spot != self.model.start:
			self.model.end = spot
			self.model.end.make_end()
			self._refresh()

		elif spot != self.model.start and spot != self.model.end:
			self.model.create_barrier(row, col)

		self._refresh()

	def clicked_right(self, pos):
		row, col = pos
		spot = self.model.get_spot(row,col)

		if spot == self.model.start:
			self.model.start = None
		elif spot == self.model.end:
			self.model.end = None

		self.model.reset_spot(row, col)
		self._refresh()

	def _refresh(self):
		self.view.refresh_display(self.model.get_spots())

	def refresh_spots(self, spots):
		self.view.refresh_display(spots)

	def main(self):
		self.view.mainloop()


if __name__== "__main__":
	c = Controller()
	c.main()
