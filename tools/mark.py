#coding=utf-8

import sys,os

def try_add(dicto,keyo,valo):
  try:
    dicto[keyo] += valo
  except:
    dicto[keyo] = valo

trigram = {}
count = {}
bigram = {}
for f in os.listdir('mark/in/'):
  cf = open(os.path.join('mark/in',f),'r')
  for line in cf:
    if line.endswith('\n'): line = line[:-1]
    arr = line.split(' ')
    try_add(trigram,(arr[0],arr[1],arr[2]),int(arr[3]))
    try_add(count,arr[1],int(arr[3]))
    try_add(bigram,(arr[0],arr[1]),int(arr[3]))
    if arr[2]=='$': try_add(bigram,(arr[1],arr[2]),int(arr[3]))
  cf.close()

bi_freq = {}
tri_freq = {}

f = open('mark/bigram.mrk','w')
for b in bigram.keys():
  f.write(b[0]+' '+b[1]+' '+str(bigram[b])+'\n')
f.close()

f = open('mark/trigram.mrk','w')
for t in trigram.keys():
  f.write(t[0]+' '+t[1]+' '+t[2]+' '+str(trigram[t])+'\n')
f.close()
  