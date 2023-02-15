import sys
import os 
from conll.conll import *
from conll.conllgrid import ConllGrid

from copy import deepcopy as copy

import npyscreen


class App(npyscreen.NPSAppManaged):
  def onStart(self):
      self.addForm("MAIN", MainForm)

  def load_con(self, fn):
    self.fn = os.path.abspath(fn)
    n_id = os.path.splitext(os.path.basename(fn))[0]
    self.con = Conll()
    self.con.load_from_file(fn)

  def save_con(self, fn):
    self.fn = fn
    self.con.update_sent_id()
    self.con.update_text()
    self.con.exportu(fn)


class MainForm(npyscreen.Form):
    def create(self):
        max_h, max_w = self.useable_space()
        self.id_field = self.add(npyscreen.FixedText, name = "Sent id")
        self.text_field = self.add(npyscreen.FixedText, max_width = max_w - 4, name = "Sent text")
        self.sega = self.add(ConllGrid, scroll_exit=False, slow_scroll=True, max_height=max_h-10, name = 'Sega', col_margin=0, columns=10)
        self.sega.create(max_x=10, max_y=0)
        self.sega.col_titles = self.parentApp.con.get_col_names()
        self.cursor_field = self.add(npyscreen.FixedText, name = "Curfield")
        self.input_text = self.add(npyscreen.FixedText, name = "Input text", hidden=True)
        self.input = self.add(npyscreen.Textfield, name = "Input", hidden=True)
        self.cur_sent = 0
        self.update_grid()
        self.load_sent()
        self.add_handlers({
            'A': self.prev_sent,
            'D': self.next_sent,
            'j': self.kunigi_sent,
            'J': self.kunigi_sent,
            'k': self.disigi_sent,
            'K': self.disigi_sent,
            '^S': self.save_menu,
            '^L': self.load_menu,
            })

    def focus(self, *args):
      self.h_exit_down(*args)

    def show_label(self):
      self.input.hidden = False
      self.input_text.hidden = False
      self.display()

    def hide_label(self):
      self.input.value =''
      self.input_text.value = ''
      self.input.hidden = True
      self.input_text.hidden = True
      self.display()

    def edit_menu(self, *args):
      self.input_text.value = 'Edit label:'
      self.input.value = self.get_value()
      self.show_label()
      self.input.edit()
      self.set_value(self.input.value)
      self.hide_label()

    def save_menu(self, *args):
      self.input_text.value = 'Save Path:'
      self.input.value = self.parentApp.fn
      self.show_label()
      self.input.edit()
      try:
        self.parentApp.save_con(self.input.value)
      except Exception as e:
        self.input_text.value = 'Error Occured! Try another address!'
        self.input.value = str(e)
        self.show_label()
        self.input.edit()
      self.hide_label()

    def load_menu(self, *args):
      self.input_text.value = 'Load Path:'
      self.input.value = self.parentApp.fn
      self.show_label()
      self.input.edit()
      try:
        self.parentApp.load_con(self.input.value)
        self.cur_sent = 0 
        self.load_sent()
      except Exception as e:
        self.input_text.value = 'Error Occured! Try another address!'
        self.input.value = str(e)
        self.show_label()
        self.input.edit()
      self.hide_label()

    def prev_sent(self, *args):

        if self.cur_sent > 0:
          self.cur_sent -= 1
          self.load_sent()

    def next_sent(self, *args):
        if self.cur_sent < self.parentApp.con.get_size()-1:
          self.cur_sent += 1
          self.load_sent()

    def kunigi_sent(self, *args):
      if self.cur_sent < self.parentApp.con.get_size()-1:
        self.parentApp.con.kunigi_sentoj(self.cur_sent)
        self.load_sent()

    def disigi_sent(self, *args):
      if self.sega.y < self.sega.max_y:
        self.parentApp.con.disigi_sentoj(self.cur_sent, self.sega.y+1)
        self.load_sent()

    def load_sent(self):
        self.sent = self.parentApp.con.get_sent(self.cur_sent)
        sent = self.sent
        self.id_field.value = sent.get_sent_id()
        self.text_field.value = sent.get_text()
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

    def copy_line(self, shift=False):
      self.sent.insert_token(copy(self.sent.tokens[self.sega.y]), self.sega.y, shift)
      self.load_sent()

    def delete_line(self, shift=False):
      self.sent.delete_token(self.sega.y, shift)
      self.load_sent()

    def exit(self, *args):
      sys.exit()
      self.parentApp.setNextForm(None)

    def AfterEditing(self):
      self.parentApp.setNextForm(None)


if __name__=='__main__':
    a = App()
    fn = '../data/hand/fe_dep_ab_1.0.2.con' if len(sys.argv)==1 else sys.argv[1]
    a.load_con(fn)
    a.run()
