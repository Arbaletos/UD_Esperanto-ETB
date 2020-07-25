#/usr/bin/python3
#coding=utf-8

import sys
import os
import re

from copy import deepcopy as copy

from conll.conll import Token, Conll, Sent

from bs4 import BeautifulSoup

from nltk import word_tokenize, sent_tokenize


def get_source(fn, root='../data'):
  if fn=='stdin':
    return fn
  if fn.endswith('.xml'):
    return os.path.join(root,'xml',fn)
  if fn.endswith('.con'):
    return os.path.join(root,'conll',fn)
  return os.path.join(root,'txt',fn)


def parse_source(source):
  """Makes text from .txt or .xml file"""
  if source=='stdin':
    text = input('Enter your text or q to exit!\n')
    if text == 'q': sys.exit()
    return text
  elif source.endswith('.xml'):
    with open(source, 'r') as reader:
      content = reader.read()
    soup = BeautifulSoup(content)
    p = soup.find_all('p')
    text = [t.get_text() for t in p]
    #Necesas parsi la fremdlangan segmentajxon
    return '\n'.join(text)
    pass
  elif source.endswith('con'):
    data = Conll()
    data.load_from_file(source)
    return [s.tokens for s in data.sentaro]
  else:
    ###All other text files.###
    with open(source, 'r') as reader:
      return reader.read()


def is_raw(fn):
  """Check whether the input is raw and thus needs preprocecing or not"""
  if fn.endswith('.con'):
    return False
  return True


def main():
  args = sys.argv[1:]
  pipeline = args[:]
  if not args: 
    pipeline.append('stdin')
  while len(pipeline):
    source = get_source(pipeline.pop())
    #out = get_out(source)
    if not is_raw(source):
      print('Cxi programo laboras nur kun nedisigita teksto')
      quit()
    text = parse_source(source)
    #text = clean_text(text)

    #sents = sent_split(text)
    #tokens = [parser.tokenize(sent) for sent in sents]
      
    #con = Conll(id=os.path.basename(source))
    #for t_sent in tokens:
    #  seg = parser.parse(t_sent)
    #  sent = build_sent(seg)
    #  con.add(sent)

    #  print(sent)
    #con.update_sent_id()
    #con.update_text()
    #con.exportu(out)

    if source == 'stdin':
      pipeline.append('stdin')
      

if __name__=='__main__':
  main()