#/usr/bin/python3
#coding=utf-8

import sys
import os

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

  
def main():
  args = sys.argv[1:]
  pipeline = args[:]

  parser = morf.MorfParser()

  if not args: 
    pipeline.append('stdin')
  while len(pipeline):
    source = get_source(pipeline.pop())
    out = get_out(source)

    if is_raw(source): # Disigado
      con = disigilo.preprilabori(source)
    else:
      con = Conll(id=os.path.splitext(os.path.basename(source))[0])
      con.load_from_file(source)

    for sent in con.sentaro:
      parser.parse(sent)
      print(sent)
 
    con.exportu(out)

    if source == 'stdin':
      pipeline.append('stdin')
      

if __name__=='__main__':
  main()
