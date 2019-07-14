#/usr/bin/python3
#coding=utf-8

"""
Author: Artemo Arbaletos
https:github.com/Arbaletos
Last change: 14.07.2019
"""


import sys
import os
import re

from copy import deepcopy as copy

from con.conll import Token
    
    
class Parser:

  def __init__(self, q_trick=False, y_trick=False, diakr_sys=False):
    """Initializes required for work dicts
    q_trick - Using of q-letter instead of ' apostrophe
    y-trick - Each foreign word is marked by y on ending
    diakr_sys - code diakr by x sistemo, h sistemo, au do not code at all.
    """
    
    ###INIT ClOSED WORDS DICT###
    num_k ={k:'NUM' for k in ['du', 'tri', 'kvar', 'kvin', 'ses', 'sep', 'ok', 'naŭ']}
    num_f ={'dek':'','cent':''}
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
        self.cls_dict[c[0]] = c[1:]
    self.cls_dict.update(kombiki(num_k,num_f))
    self.cls_dict.update(kombiki(kor_k,kor_f))
    self.cls_dict.update(kombiki(prn_k,prn_f))
    
    ###INIT OPEN WORD DICT(FIN_DICT)
    self.fin_dict = { "'":'NSN',
                 'o':'NSN','oj':'NPN','on':'NSA','ojn':'NPA',
                 'a':'ASN','aj':'APN','an':'ASA','ajn':'APA',
                 'e':'ADE','en':'ADD','as':'VPR','os':'VFT',
                 'is':'VPS','i':'VIN','u':'VDM','us':'VCN'}
    
    ###Special ending for partiples
    self.part_fin_dict = {'at':'SPR','ot':'SFT','it':'SPS',
                          'ant':'DPR','ont':'DFT','int':'DPS'}
                 
    ###INIT COVERT DICT TO CONVERT 2 TAG###
    conv_dict = {   'NSN':('NOUN',1),  'NPN':('NOUN',2),
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
          conv_dict[k+f] = ['DET',1]
        elif f in ['DPA','APA']: conv_dict[k+f] = ['DET',2]
        elif f in ['DSN','ASN','DQU','DPS']: conv_dict[k+f] = ['DET',0]
        elif f == 'PRUA': conv_dict[k+f] = ['PRON',1]
        elif f == 'PRUN': conv_dict[k+f] = ['PRON',0]
        elif f == 'ADV': conv_dict[k+f] = ['ADV',0]
        elif f == 'ADD': conv_dict[k+f] = ['ADV',1]
        
    self.conv_dict = conv_dict

    self.token_list = ['k.t.p.', 'i.e.', 'd-ro', '...']
    self.token_list = sorted(self.token_list, key=lambda x:-len(x))
    self.token_list = ['^'+t.replace('.', '\.') for t in self.token_list]
    self.token_list = self.token_list + ['^[A-Z]\.','^\d+', '^\w+','^.']
    
    
  def tokenize(self, sent):
    """Split sent into tokens sequence, with spaces also."""
    ret = []
    spaced_toks = sent.split(' ')
    cur_id = 1
    for tok in spaced_toks:
      while len(tok):
        for reg in self.token_list:
          regres = re.search(reg, tok)
          if regres is not None:
            w = regres.group(0)
            space = len(w)==len(tok)
            ret.append(Token(cur_id, w, misc={'SpaceAfter':space}))
            cur_id+=1
            tok = tok[len(w):]
            break
    #qtrick()
    return ret    
    
  def parse(self, sent, disamb=False):
    ret = []
    for i, t in enumerate(sent):
      parsoj = self.get_tag(t, i==0)
      
      for p in parsoj:
          self.get_feats(p)
          self.get_misc(p)
          ret.append(p)
    if disamb:
        ret = self.disamb(ret)
    return ret 
      
  def get_tag(self, token, new_sent):
  
    if token.is_digit():  #digital numerals
      return [self.add_pos(token, 'NUM')]
      
    if token.is_punct():  #punctuation
      return [self.add_pos(token, 'PUNCT')]
      
    if token.is_symb():  #symbol - phone, email, url, abbreviation.
      return [self.add_pos(token, 'SYM')]

    ret = []
      
    if self.cls_dict.get(token.word.lower(), None): #word from closed class
      poss = self.cls_dict[token.word.lower()]
      for pos in poss:
        tag, ind = self.conv_dict.get(pos,(pos,0))
        lemm = token.word.lower()[:len(token.word) - ind]
        ret.append(self.add_pos(token, pos, tag, lemm))
      return ret
      
    if token.is_capital() and not new_sent: #If this word definetely proper
      if token.word.endswith('on'):
        ret.append(self.add_pos(token, 'PROPN', 'PROPA', token.word[:-1]))
      ret.append(self.add_pos(token, 'PROPN'))
      
    if token.is_foreign(): #Don't parse foreign word by ending.
      return ret+[self.add_pos(token, 'X')]
      
    for fin in self.fin_dict.keys():
      if token.word.endswith(fin):
        tag = self.fin_dict[fin]
        pos, ind = self.conv_dict.get(tag,(tag,0))
        lemm = token.word.lower()[:len(token.word) - ind]
        if pos in ['ADJ','NOUN','ADV']:
          for part in self.part_fin_dict.keys():
            if lemm.endswith(part):
              tag = self.part_fin_dict[part]+tag
              break
        ret.append(self.add_pos(token, pos, tag, lemm))
        return ret
    ret.append(self.add_pos(token, 'X'))
    return ret
    
  def get_feats(self, token):
    feats = []
    fin = token.word[len(token.lemma):]
    if token.upos =='VERB':
      if token.xpos == 'VPR': feats.append('Mood=Ind|Tense=Pres')
      if token.xpos == 'VPS': feats.append('Mood=Ind|Tense=Past')
      if token.xpos == 'VFT': feats.append('Mood=Ind|Tense=Fut')
      if token.xpos == 'VCN': feats.append('Mood=Cnd')
      if token.xpos == 'VDM': feats.append('Mood=Imp')
      if token.xpos == 'VIN': feats.append('VerbForm=Inf')
    else:
      if len(token.xpos)>=1:
        if token.xpos[-1] == 'A': feats.append('Case=Acc')
        if token.xpos[-1] == 'N': feats.append('Case=Nom')
      if len(token.xpos)>=2:
        if token.xpos[-2] == 'S': feats.append('Number=Sing')
        if token.xpos[-2] == 'P': feats.append('Number=Plur')
    #Prontype for correlativoj!
    #Part for participles!
    if feats:
      token.set_feats('|'.join(feats))
      feats.clear()
    else:
      token.set_feats('_')
  
  def get_misc(self, token):
    if token.is_foreign():
          token.add_misc('Foreign=True')
      
  def add_pos(self, token, pos, tag=None, lemm=None):
    ret = copy(token)
    if tag is None:
      tag = pos
    if lemm is None:
      lemm = token.word.lower()
    ret.lemma = lemm
    ret.upos = pos
    ret.xpos = tag
    return ret
  
  
def sent_split(text):
  """Dissects text into sentences"""
  #Sent End Markers: . ! ? \n, next word begins from Capital
  start = 0
  text = text.replace('! ', '!\n').replace('? ', '?\n')
  
  for i in range(1, len(text)-2):
    if text[i]=='.':
      if text[i+1] == ' ' and text[i+2].isupper() and not text[i-1].isupper():
        text = text[:i+1]+'\n'+text[i+2:]
      #'Yes. Yes' - Du
      #'L. M. Zamenhofo' - Unu
  sents = text.split('\n')
  return sents
    
    
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


def parse_source(source):
  """Makes text from .txt or .xml file"""
  if source=='stdin':
    text = input('Enter your text or q to exit!\n')
    if text == 'q': sys.exit()
    return text
  elif source.endswith('.xml'):
    ###xml parsing routine###
    pass
  else:
    ###All other text files.###
    with open(source, 'r') as reader:
      return reader.read()


def get_out(source, root='../m_out/conll/'):
  """get output file to write for selected source"""
  if source=='stdin':
    out = open(root+'out.con', 'w')
  else:
    name = root+source.split(os.sep)[-1].replace('.xml', '').replace('.txt', '').replace('.con', '')+'.con'
    out = open(name, 'w')
  return out

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


def get_source(fn, root='../data'):
  if fn=='stdin':
    return fn
  if fn.endswith('.xml'):
    return os.path.join(root,'xml',fn)
  if fn.endswith('.con'):
    return os.path.join(root,'con',fn)
  return os.path.join(root,'txt',fn)


def build_con(sent):
  return '\n'.join([str(t) for t in sent]) + '\n'
  
  
def main():
  """Main function Loop, containing every step"""
  args = sys.argv[1:]
  pipeline = args[:]
  if not args: 
    pipeline.append('stdin')
  parser = Parser()
  while len(pipeline): 
    source = get_source(pipeline.pop())
    out = get_out(source)
    text = parse_source(source)
    text = clean_text(text)
    sents = sent_split(text)
    tokens = [parser.tokenize(sent) for sent in sents]
    for sent in tokens:
      seg = parser.parse(sent)
      con = build_con(seg)
      print(con)
      out.write(con)
    out.close()
    if source == 'stdin':
      pipeline.append('stdin')
      
      
def test():
  def ass(case, exp, real, err_name=''):
    assert exp == real, 'Test case {}: {} error, expectation "{}", reality "{}"'.format(case, err_name, exp, real)

  def testu(cases, temo, foo):
    for c in range(len(cases)):
      try:
        case = cases[c]
        foo(*[c]+case)
      except Exception as e:
        print (e)
    print ('{} {} Test Cases completed!'.format(len(cases), temo))
    
  def test_token(case, word, space, isdigit, isalpha, ispunct, issymb):
    token = Token(word=word, misc={'SpaceAfter':space}) 
    case = 'Token '+str(case)
    ass(case, word, token.word, 'word')
    ass(case, space, token.space_after(), 'space')
    ass(case, isdigit, token.is_digit(), 'is_digit')
    ass(case, isalpha, token.is_alpha(), 'is_alpha')
    ass(case, ispunct, token.is_punct(), 'is_punct')
    ass(case, issymb, token.is_symb(), 'is_symb')
  
  def test_kombiki(case, kom_dict, fin_dict, ret_dict):
    ass(case, ret_dict, kombiki(kom_dict, fin_dict))
  
  def test_sent_split(case, sent, sent_parts):
    ass(case, sent_parts, sent_split(sent))
 
  def test_tokenize(case, sent, words, spaces):
    parser = Parser()
    n_tokens = parser.tokenize(sent)
    n_words = [token.word for token in n_tokens]
    n_spaces = [token.space_after() for token in n_tokens]
    ass(case, words, n_words, 'words')
    ass(case, spaces, n_spaces, 'spaces')
    
   
  token_test_cases = [
    ['putino', True, False, True, False, False],
    ['548', True, True, False, False, False],  
    ['.', True, False, False, True, False], 
    ]
    
  kombiki_test_cases = [
    [{'a':'PUT','b':'AGUT'},{'c':'IN','d':'ARCH'},
    {'ac':['PUTIN'],'ad':['PUTARCH'],'bc':['AGUTIN'],'bd':['AGUTARCH']}],
    ]
    
  sent_split_test_cases = [
    ['Mi.', ['Mi.']],
    ['Mi estas. Hundo Kuras.', ['Mi estas.','Hundo Kuras.']],
    ['L. M. Zamenhofo', ['L. M. Zamenhofo']],
    ['Yes!\nDo, mi mortis.', ['Yes!', 'Do, mi mortis.']]
    ]
    
  tokenize_test_cases = [
    ['Mi.', ['Mi','.'],[False, True]],
    ['Hundo Kuras.', ['Hundo','Kuras','.'], [True, False, True]],
    ['L. M. Zamenhofo', ['L.', 'M.', 'Zamenhofo'],[True, True, True]],
    ]
    
  testu(token_test_cases, 'Token', test_token)
  testu(kombiki_test_cases, 'Kombiki', test_kombiki)
  testu(sent_split_test_cases, 'Sent Split', test_sent_split)
  testu(tokenize_test_cases, 'Tokenize', test_tokenize)
  
   
    
if __name__=='__main__':
  test()
  main()
