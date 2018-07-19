#/usr/bin/python3
#coding=utf-8

"""
Author: Artemo Arbaletos
https:github.com/Arbaletos
Last change: 20.05.2018
"""
import sys
import os


def parse_source(source):
  """Makes text from .txt or .xml file"""
  
  
def sent_split(text):
  """Dissects text into sentences"""
  
  
def tokenize(sent):
  """Split sent into tokens sequence, with spaces also."""

  
def get_out(source):
  """get output file to write for selected source"""
  if source=='stdin':
    out = open('../data/out/con/out.con', 'w')
  else:
    name = '../data/out/con/'+source.split(os.sep)[-1].replace('.xml','').replace('.txt','').replace('.con','')+'.con'
    out = open(name, 'w')
  return out
  
  
def main():
  """Main function Loop, containing every step"""
  args = sys.arg[1:]
  pipeline = args[:]
  if not args: pipeline = ['stdin']
  while len(pipeline): 
    source = pipeline[0]
    out = get_out(source)
    text = parse_source(source)
	sents = sent_split(text)
    tokens = [tokenize(sent) for sent in sents]
    for sent in tokens:
	  seg = morph_parse(sent)
	  con = make_con(seg)
	  out.write(con)
	out.close()
	if source != 'stdin' pipeline = pipeline[1:]
	
	
if __name__=='__main__':
  main()