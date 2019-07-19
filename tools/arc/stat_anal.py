#coding=utf-8

import sys
from conlib import *

def up(key,stat_dict):
  try:
    stat_dict[key]+=1
  except:
    stat_dict[key]=1

mark = False
filn = False

for arg in sys.argv[1:]:
  filn = arg

if not filn:
  print('No such filename')
  quit()

fn = 'con/in/'+filn+'.con'


con = parsecon(fn)
print("Word's count:" + str(len(con)))
pos = {}
tag = {}
vort = {}
stem = {}
bigram = {}

s_count = 0
for vi in range(len(con)):
  par = 3
  end = [0,'','','$','$']
  v = con[vi]
  vp = con[vi-1]
  if vi+1 == len(con) or con[vi+1][0]=='1': vn = end
  else: vn = con[vi+1]
  if v[0]=='1': 
    s_count +=1
    vp = end
  up(v[3],pos)
  up(v[4],tag)
  up(v[2].lower(),stem)
  up(v[1].lower(),vort)
  if vn[0]!=v[0]:
    up((vp[par],v[par],vn[par]),bigram)

pos_top = sorted(list(pos),key = lambda x:pos[x],reverse = True)
tag_top = sorted(list(tag),key = lambda x:tag[x],reverse = True)
stem_top = sorted(list(stem),key = lambda x:stem[x],reverse = True)
freq_top = sorted(list(bigram),key = lambda x:bigram[x],reverse = True)

stats = {'s_count':s_count,'w_count':len(con),'pos_count':pos,'tag_count':tag,'stem_count':stem,'vort_count':vort, 'freq':bigram}

f = open('mark/in/' + filn + '.mrk','w') 
for b in bigram.keys():
  f.write(b[0]+' '+b[1]+' '+b[2]+' '+str(bigram[b])+'\n')
f.close()

print('Sentences: '+ str(stats['s_count']))
print('Words: '+str(stats['w_count']))
print('Different Stems: '+str(len(stem)))
print('Different Words: '+str(len(vort)))
#print(stats['pos_count'])
#print(stats['tag_count'])

print('Top POS')
for p in pos_top:
  print('Pos:'+p+'; count:' + str(pos[p]))

print('Top TAG')
for t in tag_top:
  print('Tag:'+t+'; count:' + str(tag[t]))

print('TOP-10 STEM')
for s in stem_top[:10]:
  print('Stem:'+s+'; count:' + str(stem[s]))

print('TOP-10 BIGRAMS')
for f in freq_top[:10]:
  print('Bigram:'+str(f)+'; count:' + str(bigram[f]))
