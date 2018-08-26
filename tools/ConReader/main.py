from conll import *
import time


if __name__=='__main__':
  with open('fk.con','r') as in_con:
    start = time.time()
    spaced = insert_spaces(in_con.read())
    space = time.time()
    con = Conll(spaced, 'fund_kres_')
    init = time.time()
    con.update_sent_id()
    con.update_text()
    print(con)
    end = time.time()
    #from termcolor import colored
    #colored('hello', 'red', 'on_white'), 
    print(f'Space insert time: {space-start}, init time: {init-space}, print time: {end-init}, ful l time: {end-start}')