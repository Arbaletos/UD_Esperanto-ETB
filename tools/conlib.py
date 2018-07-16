#coding=utf-8

def parsecon(fn):
  inpu = list(map(lambda x:x.split('\t'),open(fn).read().split('\n')))
  return list(filter(lambda x: len(x)>=5, inpu))

def getsent(inp):
  for i in range(1,len(inp)):
    if inp[i][0]=='1':
      return inp[:i]
  return inp[:]

def t_in(i,listo,ind):
  """True, if listo[a][ind] = i for at least one element."""
  for a in listo:
    if a[ind]==i:
      return True
  return False