#/usr/bin/python3
#coding=utf-8

import xml.etree.ElementTree as etree
import json
import sys

TEI = '{http://www.tei-c.org/ns/1.0}'

def numparse(instr):
  """Parses esperanto numerics, and returns it's value in string, 'NaN' (not a number) , or 'NkN' (uncorrect number) """

  edict = {'nul':0,'unu':1,'du':2,'tri':3,'kvar':4,'kvin':5,'ses':6,'sep':7,'ok':8,'naŭ':9}
  mdict = {'dek':10,'cent':100,'mil':1000}
  cstr = instr[:]
  mul = 1
  cur = 0
  while len(cstr)>0:
    check = False
    for vort in edict.keys():
      if cstr.endswith(vort):
        cstr = cstr[:-len(vort)]
        cur += (mul-1)*edict[vort]
        #print ("detected " + vort)
        #print ("new string: " + cstr)
        check = True
    for vort in mdict.keys():
      if cstr.endswith(vort):
        if mul<mdict[vort]:
          check = True
          cstr = cstr[:-len(vort)]
          mul = mdict[vort]
          cur += mul
        else:
          return 'NkN'
    if check:
      continue
    return 'NaN'
#  ret = str(cur)
#  return ret
  return 'NUM'

def kombini(cstr,kom_dict, fin_dict):
  ret = []
  for kom in kom_dict.keys():
    if cstr.startswith(kom):
      for fin in fin_dict.keys():
        if cstr.endswith(fin) and len(kom)+len(fin) == len(cstr):
          ret.append(kom_dict[kom])
          ret+=fin_dict[fin]
  return ret

      
def korelativoj(instr):
  """Parses correlatives in esperanto"""
  cstr = instr[:]
  kom_dict = {'ki':'REL','i':'INDEF','ĉi':'UNI','neni':'NEG','ti':'INDIC'}
  fin_dict = {'a':['PROP','SING','NOM'], \
    'o':['MAT','NOM'],'u':['PERS','SING','NOM'], \
    'e':['LOC'],'el':['MODUS'],'en':['LOC','DIR'], \
    'es':['POSS'],'om':['COUNT'],'oma':['NUM'], \
    'am':['TEMP'],'al':['KAUZ'],'on':['MAT','ACC'], \
    'aj':['PROP','PLUR','NOM'],'an':['PROP','SING','ACC'],\
    'ajn':['PROP','PLUR','ACC'],'uj':['PERS','PLUR','NOM'],\
    'un':['PERS','SING','ACC'],'ujn':['PERS','PLUR','ACC']}
  ret = kombini(cstr,kom_dict,fin_dict)
  if len(ret) > 0:
    ret = ['KOR'] + ret
  return ret

def pronomoj(instr):
  """Parses pronouns"""
  cstr = instr[:]
  ret = []
  kom_dict = {'m':['I','SING'], \
    'v':['II'], \
    'c':['II','SING','INFORMAL'], \
    'l':['III','SING','MAS'], \
    'ŝ':['III','SING','FEM'], \
    'ĝ':['III','SING'], \
    's':['S'], \
    'n':['I','PLUR'], \
    'il':['III','PLUR'], \
    'on':[]}
  fin_dict = {'i':[], \
    'in':['ACC'], \
    'ia':['POSS'], \
    'iaj':['POSS','PLUR'], \
    'iajn':['POSS','PLUT','ACC']}
  ret = kombini(cstr,kom_dict,fin_dict)
  if len(ret) > 0:
    ret = ['PRON'] + ret[0]
  return ret

def getstem(cword,gram):
  word = cword[:].lower()
  ret = []
  cur = numparse(word)
  if cur!='NaN':
     cur = [cur]
#    gram+=['NUM',cur]
#    ret.append([word[:],gram[:]])
  else:
    cur = korelativoj(word)
  if cur==[]:
#    ret.append([word[:],cur[:]])
    cur = pronomoj(word)
#    ret.append([word[:],cur[:]])

  if len(word)==1:
    cur = ['LITER']
#    ret.append([word[:],'LITER'])
  if len(cur)>0:
    ret.append({"stem":word[:],"gram":cur[:]})
  if word in dict.keys():
#    cur+=dict[word]
#    ret.append([word[:],gram[:]])
    ret.append({"stem":word[:],"gram":dict[word]})
#  if len(cur)>0:
#  ret.append({"stem":word[:],"gram":cur[:]})
  if cword[0].isupper():
  #  ret.append([word,['NAMED_ENT']])
    ret.append({"stem":word,"gram":['NAMED_ENT']}) 
#  if len(ret)>0:
#    return ret

  if len(word)>3 or (len(word)==3 and word[-1] in ['a','e','i','o','u']):
    found = 0
    if word.endswith('as'):
      gram += ['VERB','PRESENT']
      found = 2 
    if word.endswith('is'):
      gram += ['VERB','PAST']
      found = 2 
    if word.endswith('os'):
      gram += ['VERB','FUTURE']
      found = 2 
    if word.endswith('us'):
      gram += ['VERB','COND']
      found = 2 
    if word.endswith('u'):
      gram += ['VERB','DOM']
      found = 1 
    if word.endswith('i'):
      gram += ['VERB','INF']
      found = 1 
    if word.endswith('n'):
      gram.append('ACC')
      word = word[:-1]
    if word.endswith('j'):
      gram.append('PLUR')
      word = word[:-1]
    if word.endswith('o') or word.endswith("'"):
      gram.append('NOUN')
      found = 1 
    if word.endswith('a'):
      gram.append('ADJ')
      found = 1 
    if word.endswith('e'):
      if 'PLUR' not in gram:
        gram.append('ADV')
        found = 1 
    if found > 0:
#      ret.append([word[:-found],gram[:]])
      ret.append({"stem":word[:-found],"gram":gram[:]}) 
  if len(ret)<1:
#    ret.append([word,['UNDEF']])
    ret.append({"stem":word[:],"gram":['UNDEF']}) 
#    undef.append(word) 
  return ret

def parsesent(sent):
  #undef = []
  ret = []
  words = sent.split(' ')
  cont = sent
  word = ''
  w_size = 3
  curcont = ""
  for i in range(0,len(words)):
    word = words[i]
    w_s = 0
    w_e = len(words)-1
    if w_size < i:
      w_s = i-w_size
    if i+w_size<len(words)-1:
      w_e = i - w_size
    curcont = words[w_s:w_e]
    cw = ''
#    word = word.lower()
    for c in word:
      if c.isalpha() or c=="'":
        cw = cw + c
      else:
        stem = [[c,['PUNKT']]]
        stem = [{"stem":c,"gram":['PUNKT']}] 
        print ("%s:%r" %(c, stem)) 
        ret.append({'word':c,'morph':stem})
    if len(cw)>0:
      grams = []
      stem = getstem(cw,grams)
      print ("%s:%r" %(cw, stem))
      ret.append({'word':cw,'morph':stem})

  if len(undef)>0:
    print ('Estas maldefinitaj vortoj. Ĉu vi volas Defini? (y/n)')
    if input()!='n':
      dictcsv = open("dict.csv","a")
      for word in undef:
        print ('')
        print ('Konteksto:"'+cont+'"')
        print ('Detala Konteksto:%r' % curcont)
        print ('Vorto:"'+word+'"')
        print ('Tajpu gramememoj por cxi tiu vorto aux tajpu nenion.')
        gram = input()
        if len(gram)>0:
          gram = gram.split(',')
          dict[word] = gram[:]
          dictcsv.write(','.join([word]+gram[:])+'\n')
          print("Informatio estas aldonita.")
        else:
          print("Nenio estis farita.")
  return ret
#|-------------------------->╔═╦═╗║ ║ ║╠═╬═╣╚═╩═╝

dict = {}
undef = []
out = ''

dictcsv = open("dict.csv","r")

for line in dictcsv:
  c = line[:-1].split(',')
  dict[c[0]] = c[1:]
  dict['mal'+c[0]] = c[1:]
dictcsv.close()

for i in range (1, len(sys.argv)):
  filename = 'corp/in/'+sys.argv[i]+'.xml'
  out = open('out/'+sys.argv[i]+'.json',"w")
  tree = etree.parse(filename)
  root = tree.getroot()
  out.write('[')
  for s in tree.iter(tag = TEI+'p'):
    if len(s.text) > 0:
      out.write('[')
      out.write(json.dumps(parsesent(s.text)))
      out.write(']')
    undef = []
  out.write(']')
  out.close
out = open('out/stdout.json',"w")
out.write('[')
while True:
  sent = input("Input esperanto sentense or q to exit!\n")
  if (sent=='q'):
    out.write(']')
    out.close()
    exit()
  out.write('[')
#  print(parsesent(sent))
  ret = parsesent(sent)
  print (json.dumps(ret, indent=2))
  out.write(json.dumps(ret))
  out.write(']')
  undef = []


