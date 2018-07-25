#/usr/bin/python3
#coding=utf-8

"""
Author: Artemo Arbaletos
https:github.com/Arbaletos
Last change: 25.07.2018
"""
import sys
import os

class Token:

  def __init__(self, word, space=True)
    self.word = word      #form of word in text
    self.space = space    #is this token followed by space?
    self.vars = []
    
    
class Parser:

  def __init__(self, q_trick=False, y_trick=False, diakr_sys=False):
    """Initializes required for work dicts
    q_trick - Using of q-letter instead of ' apostrophe
    y-trick - Each foreign word is marked by y on ending
    diakr_sys - code diakr by x sistemo, h sistemo, au do not code at all.
    """
    
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
    
    ###INIT ClOSED WORDS DICT###
    num_k ={k:'NUM' for k in ['du', 'tri', 'kvar', 'kvin', 'ses', 'sep', 'ok', 'naŭ']}
    num_f ={'dek':'','cent':''}
    #kor_k = {'ki':'INT','i':'IND','ĉi':'IND','neni':'IND','ti':'DEM'}
    kor_k = {'ki':'DEM','i':'KOR','ĉi':'KOR','neni':'KOR','ti':'KOR'}
    kor_f = {'a':'ASN', 'o':'PRUN', 'u':'DSN', 'e':'ADV','el':'ADV',\
             'en':'ADD', 'es':'DPS','om':'DQU', 'am':'ADV','al':'ADV',\
             'on':'PRUA', 'aj':'APN','an':'ASA','ajn':'APA','uj':'DPN',\
             'un':'DSA','ujn':'DPA'}
    prn_k = {'m':'PRS', 'v':'PRU', 'c':'PRS', 'l':'PRS','ŝ':'PRS',\ 
             'ĝ':'PRS', 's':'PRS', 'n':'PRP', 'il':'PRP', 'on':'PRP'}
    prn_f = {'i':'N', 'in':'A', 'ia':'PSN', 'ian':'PSA', \
             'iaj':'PPN', 'iajn':'PPA'}
             
    self.cls_dict = {}
    with open("dict.csv") as dictcsv:
      for line in dictcsv:
        c = line[:-1].split(',')
        self.dict[c[0]] = c[1:]
    self.cls_dict.update(kombiki(num_k,num_f))
    self.cls_dict.update(kombiki(kor_k,kor_f))
    self.cls_dict.update(kombiki(prn_k,prn_f))
    
    ###INIT OPEN WORD DICT(FIN_DICT)
    self.fin_dict = { "'":'NSN',"q":"NSN",
                 'o':'NSN','oj':'NPN','on':'NSA','ojn':'NPA',
                 'a':'ASN','aj':'APN','an':'ASA','ajn':'APA',
                 'e':'ADE','en':'ADD','as':'VPR','os':'VFT',
                 'is':'VPS','i':'VIN','u':'VDM','us':'VCN'}
                 
    ###INIT COVERT DICT TO CONVERT 2 TAG###
    convert_dict = {   'NSN':('NOUN',1),  'NPN':('NOUN',2),
    'NSA':('NOUN',2),  'NPA':('NOUN',3),  'ASN':('ADJ',1),
    'APN':('ADJ',2),   'ASA':('ADJ',2),   'APA':('ADJ',3),
    'ADE':('ADV',1),   'ADD':('ADV',2),   'VPR':('VERB',2),
    'VFT':('VERB',2),  'VPS':('VERB',2),  'VIN':('VERB',1),
    'VDM':('VERB',1),  'VCN':('VERB',2),  
    'PRSN':('PRON',0), 'PRPN':('PRON',0),'PRUN':('PRUN',0),
    'PRSA':('PRON',1), 'PRPA':('PRON',1),'PRUA':('PRON',1),
    'PRSPSN':('DET',1),'PRPPSN':('DET',1),'PRUPSN':('DET',1), 
    'PRSPSA':('DET',2),'PRPPSA':('DET',2),'PRUPSA':('DET',2),
    'PRSPPN':('DET',2),'PRPPPN':('DET',2),'PRUPPN':('DET',2), 
    'PRSPPA':('DET',3),'PRPPPA':('DET',3),'PRUPPA':('DET',3),
    'PROPN':('PROPN',0), 'PROPA':('PROPN',1)}

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
        
    self.conv_dict = convert_dict
    
    
  def tokenize(self, sent):
  """Split sent into tokens sequence, with spaces also."""
  ###Replace by spacy###
    ret = []
    tokens = magic()
    tokens = Token(magic)
    #qtrick()
    return ret    
    
  def parse(self, sent):
    for i in range(len(sent)):
      id = i+1
      t = sent[i]
      t.id = id
      self.get_tag(t,i==0)
      #self.get_feats(t) #Not realized
    return sent
      
  def get_tag(self, token, new_sent):
  
    if token.is_digit():  #digital numerals
      self.addVar(token, 'NUM')
      return
      
    if token.is_punct():  #punctuation
      self.addVar(token, 'PUNCT')
      return
      
    if token.is_symb():  #symbol - phone, email, url, abbreviation.
      self.addVar(token, 'SYM')
      return
      
    if self.cls_dict.get(token.word.lower(),None): #word from closed class
      poss = self.cls_dict[token.word.lower()]
      for pos in poss:
        tag, ind = self.conv_dict.get(pos,(pos,0))
        lemm = token.word.lower()[:len(token.word) - ind]
        self.addVar(token, pos, tag, lemm)
      return
      
    if token.is_capital() and not new_sent: #If this word definetely proper
      if token.word.endswith('on'):
        self.addVar(token, 'PROPN', 'PROPA', token.word[:-1])
        return
      if token.is_foreign():
        token.foreign = True
      self.addVar(token, 'PROPN')
      
    if token.is_foreign(): #Don't parse foreign word by ending.
      token.foreign = True
      self.addVar(token, 'X')
      return
      
    for fin in self.fin_dict.keys():
      if token.word.endswith(fin):
        pos = self.fin_dict[fin]
        tag, ind = self.conv_dict.get(pos,(pos,0))
        lemm = token.word.lower()[:len(token.word) - ind]
        self.addVar(token, pos, tag, lemm)
        return
    self.addVar(token, 'X')
    return
      
      
  def addVar(self, token, pos, tag=None, lemm=None):
    if tag is None:
      tag = pos
    if lemm is None:
      lemm = token.word.lower()
    token.vars.append((lemm, pos, tag))
    

def parse_source(source):
  """Makes text from .txt or .xml file"""
  if source=='stdin':
    text = input('Enter your text or q to exit!')
    if text=='q': sys.exit()
    return text
  elif source.endswith('.xml'):
    ###xml parsing routine###
    pass
  else:
    ###All other text files.###
    with open(source,'r') as inf:
      return inf.read()
  
  
def sent_split(text):
  """Dissects text into sentences"""
  #Sent End Markers: . ! ? \n, next word begins from Capital
  sents = []
  start = 0
  for i in range(len(text)):
    ns = False
    if text[i] = '\n': ns = True
    if text[i] in ['.','!','?']:
      if i+2 < len(text):
        if text[i+1]==' ' and text[i+2].isupper:
          ns = True
    if text[i] == '.': #L. M. Zamenhofo abbreviation dodge.
      if text[i-1].isupper:
        ns = False
    if ns:
      sents.append(text[start,i+1])
      start = i+1
    
  
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
  if not args: pipeline.append('stdin')
  parser = Parser()
  while len(pipeline): 
    source = pipeline.pop()
    out = get_out(source)
    text = parse_source(source)
    sents = sent_split(text)
    tokens = [parser.tokenize(sent) for sent in sents]
    for sent in tokens:
      seg = parser.parse(sent)
      con = make_con(seg)
      out.write(con)
    out.close()
    if source == 'stdin' pipeline.append('stdin')
    
    
if __name__=='__main__':
  main()
