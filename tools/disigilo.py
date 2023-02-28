#/usr/bin/python3
#coding=utf-8

import click
import sys
import os
import re
import click

from conll.conll import Token, Conll, Sent

from bs4 import BeautifulSoup

from nltk import word_tokenize, sent_tokenize

import ilo


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

def clean_text(text):
    """Sxangxos la x-sisteme skribitaj cxapelliteroj per cxapele skribitaj"""
    dicto = {'Cx':'Ĉ',
             'Gx':'Ĝ',
             'Hx':'Ĥ',
             'Jx':'Ĵ',
             'Sx':'Ŝ',
             'Ux':'Ŭ'} # POZOR! tux -> tŭ!!!
    for k in dicto:
        text = text.replace(k, dicto[k])
        text = text.replace(k.lower(), dicto[k].lower())
        text = text.replace(k.upper(), dicto[k].upper())
    return text


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

def preprilabori(source):

    #token_list = ['k.t.p.', 'i.e.', 'd-ro', '...']
    #token_list = sorted(token_list, key=lambda x:-len(x))
    #token_list = ['^'+t.replace('.', '\.') for t in token_list]
    #token_list += ['^[A-Z]\.','^\d+', '^\w+','^.']

    teksto = parse_source(source)
    #teksto = clean_text(teksto)
    sents = sent_tokenize(teksto)
    tokens = [disigi(sent) for sent in sents]
    con = Conll()
    for t_sent in tokens:
      sent = build_sent(t_sent)
      con.add(sent)

    con.update_sent_id()
    con.update_text()

    return con
    
@click.command
@click.option('-i', '--input', default=None, type=click.Path())
@click.option('-o', '--output', default=None, type=click.Path())
def main(input, output):
  if input is None:
    input = 'stdin'
  if output is None:
    output = 'stdout'
  while True:
    source = input
    
    if not ilo.is_raw(source):
      print('Cxi programo laboras nur kun nedisigita teksto')
      quit()
      
    con = preprilabori(source)
    
    if output == 'stdout':
        print(con)
    else:
        con.exportu(output)
    
    if input != 'stdin':
        break

if __name__=='__main__':
  main()