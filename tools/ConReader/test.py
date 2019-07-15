import sys

sys.path.append('../con')

from conll import *
import time


if __name__=='__main__':
  con = Conll(id='lesson_60')
  con.load_from_file('../../out/conll/lesson_60.con')
  sent = con.sentaro[0]
  print('sent id: ', sent.get_sent_id())
  print('sent_text: ',sent.get_text())
  print('values: ')
  print(sent.get_values())
