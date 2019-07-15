import sys

sys.path.append('../con')

from conll import *

import npyscreen
import curses

def length_split(text, max_len):
  ret = []    
  while len(text):
    ret.append(text[:max_len])
    text = text[max_len:]
  return ret


class App(npyscreen.NPSAppManaged):
  def onStart(self):
      self.con = Conll(id='lesson_60')
      self.con.load_from_file('../../out/conll/lesson_60.con')
      self.addForm("MAIN", MainForm)
      self.addForm("EDIT", EditForm)


class ConllGrid(npyscreen.GridColTitles):
  def create(self, max_x=0, max_y=0):
    self.x = 0
    self.y = 0
    self.info = ''
    self.max_x = max_x
    self.max_y = max_y
    self.y_pad = 2
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
        'r': self.edit_mode,
        'x': self.delete,
        })

  def delete(self, *args):
    self.parent.set_value('_')
    

  def edit_mode(self, *args):
    self.parent.parentApp.getForm('EDIT').value = None
    self.parent.parentApp.switchForm('EDIT')

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
    if self.x <= 0:
      return
    self.info = args
    self.x -= 1
    self.h_move_cell_left(*args)
    self.parent.update_grid()

  def move_right(self, *args):
    if self.x >= self.max_x - 1:
      return
    self.info = args
    self.x += 1
    self.h_move_cell_right(*args)
    self.parent.update_grid()

class EditForm(npyscreen.ActionPopup):
    def create(self):
        self.text_field = self.add(npyscreen.Textfield, name = "Text Field")

    def beforeEditing(self):
        val = self.parentApp.getForm('MAIN').get_value()
        self.text_field.value=val

    def on_ok(self):
      self.parentApp.getForm('MAIN').set_value(self.text_field.value)
      self.parentApp.switchFormPrevious()

    def on_cancel(self):
      self.parentApp.switchFormPrevious()


class MainForm(npyscreen.Form):
    def create(self):
        max_h, max_w = self.useable_space()
        self.id_field = self.add(npyscreen.FixedText, name = "Sent id")
        self.text_filed = self.add(npyscreen.FixedText, max_width = max_w - 4, name = "Sent text")
        self.sega = self.add(ConllGrid, scroll_exit=False, slow_scroll=True, max_height=max_h-8, name = 'Sega', col_margin=0, columns=10)
        self.sega.create(max_x=10, max_y=0)
        self.sega.col_titles = self.parentApp.con.get_col_names()
        self.cursor_field = self.add(npyscreen.FixedText, name = "Curfield")
        self.cur_sent = 0
        self.update_grid()
        self.load_sent()
        self.add_handlers({
            'A': self.prev_sent,
            'D': self.next_sent,
            })

    def prev_sent(self, *args):

        if self.cur_sent > 0:
          self.cur_sent -= 1
          self.load_sent()

    def next_sent(self, *args):
        if self.cur_sent < self.parentApp.con.get_size()-1:
          self.cur_sent += 1
          self.load_sent()

    def load_sent(self):
        self.sent = self.parentApp.con.get_sent(self.cur_sent)
        sent = self.sent
        self.id_field.value = sent.get_sent_id()
        self.text_filed.value = sent.get_text()
        self.sega.values = sent.get_values()
        self.sega.max_y = len(self.sega.values)
        self.display()

    def update_grid(self):
        self.cursor_field.value = str(self.sega.x)+':'+str(self.sega.y)
        self.display()

    def get_x(self):
      return self.sega.x

    def get_y(self):
      return self.sega.y

    def get_value(self):
      return str(self.sent.tokens[self.sega.y][self.sega.x])

    def set_value(self, value):
      self.sent.tokens[self.sega.y][self.sega.x] = value
      self.load_sent()

    def exit(self, *args):
      sys.exit()
      self.parentApp.setNextForm(None)

if __name__=='__main__':
    a = App()
    a.run()
