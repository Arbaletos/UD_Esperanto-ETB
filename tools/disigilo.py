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


def get_out(source, root='../out/conll/'):
  """get output filename to write for selected source"""
  if source=='stdin':
    name = root + 'out.con'
  else:
    name = root+source.split(os.sep)[-1].replace('.xml', '').replace('.txt', '').replace('.con', '')+'.con'
  return name


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
    # Necesas parsi la fremdlangan segmentajxon
    return '\n'.join(text)
    pass
  elif source.endswith('con'):
    data = Conll()
    data.load_from_file(source)
    return [s.tokens for s in data.sentaro]
  else:
    ### All other text files. ###
    with open(source, 'r') as reader:
      return reader.read()


def is_raw(fn):
  """Check whether the input is raw and thus needs preprocecing or not"""
  if fn.endswith('.con'):
    return False
  return True


def build_sent(sent):
  ret = Sent()
  for s in sent:
    ret.add(s)
  return ret


def disigi(sent, token_regexp=None):
  """Split sent into tokens sequence, mentioning spaces."""
  # Necesas prilabori d-ro, k.t.p., k. t. p., e-posxton, retejoj, telefonnumeroj k.t.p.
  ret = []
  spaced = sent.split(' ')
  cur_id = 1;
  for token_group in spaced:
    token_group = word_tokenize(token_group)
    for i, t in enumerate(token_group):
      ret.append(Token(cur_id, t, misc={'SpaceAfter': i==len(token_group)-1}))
      cur_id+=1
  return ret
    

def main():
  args = sys.argv[1:]
  pipeline = args[:]

  #token_list = ['k.t.p.', 'i.e.', 'd-ro', '...']
  #token_list = sorted(token_list, key=lambda x:-len(x))
  #token_list = ['^'+t.replace('.', '\.') for t in token_list]
  #token_list += ['^[A-Z]\.','^\d+', '^\w+','^.']

  if not args: 
    pipeline.append('stdin')
  while len(pipeline):
    source = get_source(pipeline.pop())
    out = get_out(source)
    if not is_raw(source):
      print('Cxi programo laboras nur kun nedisigita teksto')
      quit()
    text = parse_source(source)

    sents = sent_tokenize(text)
    tokens = [disigi(sent) for sent in sents]
      
    con = Conll(id=os.path.basename(source))
    for t_sent in tokens:
      sent = build_sent(t_sent)
      con.add(sent)

      print(sent)
    
    con.update_sent_id()
    con.update_text()
    con.exportu(out)

    if source == 'stdin':
      pipeline.append('stdin')
      

if __name__=='__main__':
  main()