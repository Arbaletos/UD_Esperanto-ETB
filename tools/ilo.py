#/usr/bin/python3
#coding=utf-8

import sys
import os
import click

from conll.conll import Token, Conll, Sent

import disigilo
import morf


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
  else:
    ### All other text files. ###
    with open(source, 'r') as reader:
      return reader.read()

def is_raw(fn):
  """Check whether the input is raw and thus needs preprocecing or not"""
  if fn.endswith('.con'):
    return False
  return True

      
@click.command
@click.option('-i', '--input', default=None, type=click.Path())
@click.option('-o', '--output', default=None, type=click.Path())
def main(input, output):
  if input is None:
    input = 'stdin'
  if output is None:
    output = 'stdout'
    
  parser = morf.MorfParser()
    
  while True:
    source = input
    if is_raw(source): # Disigado
      con = disigilo.preprilabori(source)
    else:
      con = Conll()
      con.load_from_file(source)
      
    for idx, sent in enumerate(con.sentaro):
      sent = parser.parse(sent)
      con.sentaro[idx] = sent
    
    if output == 'stdout':
        print(con)
    else:
        con.exportu(output)
    
    if input != 'stdin':
        break

if __name__=='__main__':
  main()
