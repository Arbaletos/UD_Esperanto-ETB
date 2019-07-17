import sys

sys.path.append('../con')

from conll import *
from conllgrid import ConllGrid

from copy import deepcopy as copy

import npyscreen

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
            'j': self.kunigi_sent,
            'J': self.kunigi_sent,
            'k': self.disigi_sent,
            'K': self.disigi_sent,
            })

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

    def copy_line(self, shift=False):
      self.sent.insert_token(copy(self.sent.tokens[self.sega.y]), self.sega.y, shift)
      self.load_sent()

    def delete_line(self, shift=False):
      self.sent.delete_token(self.sega.y, shift)
      self.load_sent()

    def exit(self, *args):
      sys.exit()
      self.parentApp.setNextForm(None)

if __name__=='__main__':
    a = App()
    a.run()
