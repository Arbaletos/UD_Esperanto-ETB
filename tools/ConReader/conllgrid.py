import npyscreen
import curses

class ConllGrid(npyscreen.GridColTitles):
  def create(self, max_x=0, max_y=0):
    self.x = 0
    self.y = 0
    self.info = ''
    self.max_x = max_x
    self.max_y = max_y
    self.columns = max_x+1
    self.y_pad = 2
    self.last_i = 0
    self.mode = 'DEFAULT'
    self.add_handlers({
        'a': self.move_left,
        'd': self.move_right,
        'w': self.move_up,
        's': self.move_down,
        curses.KEY_LEFT: self.move_left,
        curses.KEY_RIGHT: self.move_right,
        curses.KEY_UP: self.move_up,
        curses.KEY_DOWN: self.move_down,
        'W': self.page_up,
        'S': self.page_down,
        'r': self.parent.edit_menu,
        'x': self.delete_value,
        'c': self.delete_line,
        'C': self.delete_line_shift,
        'v': self.copy_line,
        'V': self.copy_line_shift,
        'j': self.parent.kunigi_sent,
        'J': self.parent.kunigi_sent,
        'k': self.parent.disigi_sent,
        'K': self.parent.disigi_sent,

        })

  def custom_print_cell(self, cell, value):

    if cell.relx == self.relx:
      if value == self.last_i:
        self.mode = 'CRITICAL'
      else:
        self.mode = 'DEFAULT'
      self.last_i = value

    cell.color = self.mode
    #cell.value = self.i
    #self.i += 1

  def delete_line(self, *args):
    if self.y < self.max_y:
      self.parent.delete_line(False)

  def delete_line_shift(self, *args):
    if self.y < self.max_y:
      self.parent.delete_line(True)

  def copy_line(self, *args):
    if self.y < self.max_y:
      self.parent.copy_line(False)

  def copy_line_shift(self, *args):
    if self.y < self.max_y:
      self.parent.copy_line(True)

  def delete_value(self, *args):
    self.parent.set_value('_')
    
  def page_up(self, *args):
    mh = self.max_height - self.y_pad
    if self.y <= mh:
      return
    self.y -= mh
    self.h_move_page_up(*args)
    self.parent.update_grid()

  def page_down(self, *args):
   mh = self.max_height - self.y_pad
   if self.y + mh >= self.max_y:
     return
   self.y += mh
   self.h_move_page_down(*args)
   self.parent.update_grid()

  def move_up(self, *args):
    if self.y <= 0:
      return
    self.info = args
    self.y -= 1
    self.h_move_line_up(*args)
    self.parent.update_grid()

  def move_down(self, *args):
    if self.y >= self.max_y - 1:
      return
    self.info = args
    self.y += 1
    self.h_move_line_down(*args)
    self.parent.update_grid()

  def move_left(self, *args):
    if self.x <= 0 or self.y >= self.max_y:
      return
    self.info = args
    self.x -= 1
    self.h_move_cell_left(*args)
    self.parent.update_grid()

  def move_right(self, *args):
    if self.x >= self.max_x - 1 or self.y >= self.max_y:
      return
    self.info = args
    self.x += 1
    self.h_move_cell_right(*args)
    self.parent.update_grid()
