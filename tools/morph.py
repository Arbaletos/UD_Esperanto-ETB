#/usr/bin/python3
#coding=utf-8

"""
Author: Artemo Arbaletos
https:github.com/Arbaletos
Last change: 20.05.2018
"""

try:
  import xml.etree.cElementTree as etree
except ImportError:
  import xml.etree.ElementTree as etree
import json
import sys
from spacy.lang.eo import Esperanto

TEI = '{http://www.tei-c.org/ns/1.0}'

def kombiki(kom_dict, fin_dict):
  """Combination of dict beginnings and endings"""
  ret = {}
  for kom in kom_dict.keys():
    for fin in fin_dict.keys():
      try:
        ret[kom+fin].append(kom_dict[kom]+fin_dict[fin])
      except:
        ret[kom+fin] = [kom_dict[kom]+fin_dict[fin]]  
  return ret

def qtrick(text):
  """Q-ending mark of words ending with ' """
  i = 0
  qu = False
  ret = text
  while text.find("'",i+1)>=0:
    i = text.find("'",i+1)
    if qu:
      qu = False
      continue
    if text[i-1].isalpha():
      ret = text[:i]+'q'+text[i+1:]
    else:
      qu = True
  return ret

def gettag(cword):
  """Computing tag feature"""
  ret = []
  global new_sent
  upper = cword.text[0].isupper()
  word = cword.text[:].lower()

  if cword.is_digit:
    return ['NUM']
  if cword.is_punct:
    return ['PUNCT']

  if not new_sent and upper:
    nomo = cword.text
    ACC = False
    if cword.text.endswith('y'):
      return(['PROPN'])
    if nomo.endswith('on'):
      print ('in putin we trust!')
      nomo = nomo[:-1]
      ACC = True
    if nomo not in names_list:
      names_list.append(nomo)
    if ACC:
      return(['PROPA'])
    return(['PROPN']) 
  new_sent = False

  if len(word)==1 or cword.text[-1]=='.':
    ret = ['SYM']
  try:
    ret+=dict[word]
  except:
    pass

  if len(ret)==0:
    for fin in fin_dict.keys():
      if word.endswith(fin):
        ret+=[fin_dict[fin]]
  if len(ret)==0:
    if upper:
      nomo = cword.text
      ACC = False
      if nomo.endswith('on'):
        nomo = nomo[:-1]
        ACC = True
      if nomo not in names_list:
        names_list.append(nomo)
      if ACC:
        return(['PROPA'])
      return(['PROPN']) 
    return(['X'])
  return ret

def postparse(sent):
  """Removing disambiguity, returning y-trick"""
  ret = []
  for ent_i in range(len(sent)):
      ent = sent[ent_i]
      if ent[1] in names_list:
        ent[2] = ['PROPN']
      if ent[1].endswith('y'):
        ent[1] = ent[1][0:-1]
      else:
        if ent[1].endswith('q'):
          ent[1] = ent[1][0:-1]+"'"
      if mark and len(ent[2])>1:
        curs = sent+[[0,0,['$']]]
        ps = convert_dict.get(curs[ent_i-1][2][0],[curs[ent_i-1][2][0]])[0]
        ns = convert_dict.get(curs[ent_i+1][2][0],[curs[ent_i+1][2][0]])[0]
        freq = [trigram.get((ps, convert_dict.get(ent[2][x],[ent[2][x]])[0],ns),0) for x in range(len(ent[2]))]
        ent[2] = [ent[2][freq.index(max(freq))]]
      for tag in ent[2]:
        if not tag: continue
        ret.append([])
        ret[-1].append(str(ent[0])) 
        ret[-1].append(ent[1].lower())
        ret[-1].append(ent[1][0:len(ent[1])-convert_dict.get(tag,[0,0])[1]].lower())
        ret[-1].append(convert_dict.get(tag,[tag])[0])
        ret[-1].append(tag)
  return ret

def parsesent(sent):
  """Main parse loop"""
  ret = []
  sent = qtrick(sent)
  words = nlp(sent)
  cont = sent
  id = 1
  global new_sent
  new_sent = True
  comm_dict = {'"':False,"'":False}
  for word in words:
    ret.append([id,word.text,gettag(word)])
    id+=1
    if word.text[0] in comm_dict.keys():
      if comm_dict[word.text[0]]:
        comm_dict[word.text[0]] = False
      else:
        comm_dict[word.text[0]] = True
        new_sent = True
        id = 1
    if word.text[0] in ['.','!','?']:
      new_sent = True
      id = 1
  return postparse(ret)

def output(conl):
  """Writing results"""
  for i in conl:
    s = '\t'.join(i)
    print(s)
    out.write(s+'\n')
#  out.write('\n')

def init_dict(dict):
  """Generting Tag Dictionary"""
  num_k ={k:'NUM' for k in ['du','tri','kvar','kvin','ses','sep','ok','naŭ']}
  num_f ={'dek':'','cent':''}
#  kor_k = {'ki':'INT','i':'IND','ĉi':'TOT','neni':'NEG','ti':'DEM'}
  kor_k = {'ki':'INT','i':'IND','ĉi':'IND','neni':'IND','ti':'DEM'}
  kor_f = {'a':'ASN', \
    'o':'PRUN','u':'DSN', \
    'e':'ADV','el':'ADV','en':'ADD', \
    'es':'DPS','om':'DQU', \
    'am':'ADV','al':'ADV','on':'PRUA', \
    'aj':'APN','an':'ASA',\
    'ajn':'APA','uj':'DPN',\
    'un':'DSA','ujn':'DPA'}
  prn_k = {'m':'PRS',
    'v':'PRU', \
    'c':'PRS', \
    'l':'PRS', \
    'ŝ':'PRS', \
    'ĝ':'PRS', \
    's':'PRS', \
    'n':'PRP', \
    'il':'PRP', \
    'on':'PRP'}
  prn_f = {'i':'N', \
    'in':'A', \
    'ia':'PSN', \
    'ian':'PSA', \
    'iaj':'PPN', \
    'iajn':'PPA'}
  with open("dict.csv") as dictcsv:
    for line in dictcsv:
      c = line[:-1].split(',')
      dict[c[0]] = c[1:]
    dict.update(kombiki(num_k,num_f))
    dict.update(kombiki(kor_k,kor_f))
    dict.update(kombiki(prn_k,prn_f))
 
from time import time
now = time()
dict = {}
names_list = []
undef = []
out = ''
nlp = Esperanto()

convert_dict = {   'NSN':['NOUN',1],  'NPN':['NOUN',2],
'NSA':['NOUN',2],  'NPA':['NOUN',3],  'ASN':['ADJ',1],
'APN':['ADJ',2],   'ASA':['ADJ',2],   'APA':['ADJ',3],
'ADE':['ADV',1],   'ADD':['ADV',2],   'VPR':['VERB',2],
'VFT':['VERB',2],  'VPS':['VERB',2],  'VIN':['VERB',1],
'VDM':['VERB',1],  'VCN':['VERB',2],  
'PRSN':['PRON',0], 'PRPN':['PRON',0],'PRUN':['PRUN',0],
'PRSA':['PRON',1], 'PRPA':['PRON',1],'PRUA':['PRON',1],
'PRSPSN':['DET',1],'PRPPSN':['DET',1],'PRUPSN':['DET',1], 
'PRSPSA':['DET',2],'PRPPSA':['DET',2],'PRUPSA':['DET',2],
'PRSPPN':['DET',2],'PRPPPN':['DET',2],'PRUPPN':['DET',2], 
'PRSPPA':['DET',3],'PRPPPA':['DET',3],'PRUPPA':['DET',3],
'PROPN':['PROPN',0], 'PROPA':['PROPN',1]}

kom = ['INT','IND','TOT','NEG','DEM']
fin = ['ASN','PRUN','DSN','ADV','ADV',\
  'ADD','DPS','DQU','ADV','ADV','PRUA',\
  'APN','ASA','APA','DPN','DSA','DPA']

for k in kom:
  for f in fin:
    if f in ['APN','ASA','DPN','DSA']:
      convert_dict[k+f] = ['DET',1]
    elif f in ['DPA','APA']: convert_dict[k+f] = ['DET',2]
    elif f in ['DSN','ASN','DQU','DPS']: convert_dict[k+f] = ['DET',0]
    elif f == 'PRUA': convert_dict[k+f] = ['PRON',1]
    elif f == 'PRUN': convert_dict[k+f] = ['PRON',0]
    elif f == 'ADV': convert_dict[k+f] = ['ADV',0]
    elif f == 'ADD': convert_dict[k+f] = ['ADV',1]

fin_dict = { "'":'NSN',"q":"NSN",
'o':'NSN','oj':'NPN','on':'NSA','ojn':'NPA',
'a':'ASN','aj':'APN','an':'ASA','ajn':'APA',
'e':'ADE','en':'ADD','as':'VPR','os':'VFT',
'is':'VPS','i':'VIN','u':'VDM','us':'VCN'}

init_dict(dict)

print (dict)
mark = False

args = sys.argv[1:]
trigram = {}
bigram = {}
if '-m' in args:
  mark = True
  args = args[1:]
  with open('mark/trigram.mrk') as f:
    for line in f:
      if line.endswith('\n'): line = line[:-1]
      arr = line.split(' ')
      trigram[(arr[0],arr[1],arr[2])] = int(arr[3])
    
for f in (args):
  if f.endswith('.xml'):
    filename = 'xml/in/'+f
    out = open('con/in/'+f[:-4]+'.con',"w")
    tree = etree.parse(filename)
    root = tree.getroot()
    for s in tree.iter(tag = TEI+'p'):
      text = s.text
      if text==None: text = ''
      for t in s:
        if t.text:
          c = t.text.split()
          for i in range(len(c)):
            c[i] = c[i]+'y'
#It is 'y-trick' - as a q-trick, aber anderer.
          if c: text+=' '.join(c)
          if t.tail: text+=t.tail
      if len(text) > 0:
          output(parsesent(text))
    out.close()
  else:
    with open('txt/in/'+f) as in_f:
      out = open('con/in/'+f+'.con','w')
      for line in in_f:
        if line.endswith('\n'): line = line[:-1]
        output(parsesent(line))
      out.close()

if not args:
  out = open('con/in/stdout.con',"w")
  while True: 
    sent = input("Input esperanto sentense or q to exit!\n")
    if (sent=='q'):
      out.close()
      exit()
    output(parsesent(sent))
    undef = []

print('Time elapsed:'+str(time() - now))
