import sys

sys.path.append('../con')

from conll import *

import npyscreen

def length_split(text, max_len):
  ret = []    
  while len(text):
    ret.append(text[:max_len])
    text = text[max_len:]
  return ret


class App(npyscreen.NPSAppManaged):
  def onStart(self):
      #self.registerForm("MAIN", MainForm())
      self.con = Conll(id='lesson_60')
      self.con.load_from_file('../../out/conll/lesson_60.con')
      self.addForm("MAIN", MainForm)
      

class MainForm(npyscreen.Form):
    def create(self):
        max_h, max_w = self.useable_space()
        self.id_field = self.add(npyscreen.FixedText, name = "Sent id")
        self.text_filed = self.add(npyscreen.FixedText, max_width = max_w - 4, name = "Sent text")
        self.sega = self.add(npyscreen.SimpleGrid, name = 'Sega', col_margin=0, columns=10)
        self.cur_sent = 0
        self.load_sent()

        self.add_handlers({
            'w': self.prev_sent,
            's': self.next_sent
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
        sent = self.parentApp.con.get_sent(self.cur_sent)

        self.id_field.value = sent.get_sent_id()
        self.text_filed.value = sent.get_text()
        self.sega.values = sent.get_values()
        self.display()

    def afterEditing(self):
        self.parentApp.setNextForm(None)

if __name__=='__main__':
    a = App()
    a.run()
