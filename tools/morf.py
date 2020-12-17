#/usr/bin/python3
#coding=utf-8


import sys
import os

from copy import deepcopy as copy

from conll.conll import Token, Conll, Sent

import ilo
    
    
class MorfParser:

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
    
    ### Special ending for partiples
    self.part_fin_dict = {'at':'SPR','ot':'SFT','it':'SPS',
                          'ant':'DPR','ont':'DFT','int':'DPS'}
                 
    ### INIT COVERT DICT TO CONVERT 2 TAG ###
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
    'PROPSN':('PROPN',0), 'PROPSA':('PROPN',1)}

    kom = ['KOR','DEM']
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
    
  def parse(self, sent, disamb=False):
    ret = []
    for i, t in enumerate(sent.tokens):
      parsoj = self.get_tag(t, i==0)
      
      for p in parsoj:
          self.get_feats(p)
          self.get_misc(p)
          ret.append(p)
    if disamb:
        ret = self.disamb(ret)
    sent.tokens = ret ## Faru interfacon
    return ret 
      
  def get_tag(self, token, new_sent):
  
    if token.is_digit():  #digital numerals
      return [self.add_pos(token, 'NUM')]
      
    if token.is_punct():  #punctuation
      return [self.add_pos(token, 'PUNCT')]
      
    if token.is_symb():  #symbol - phone, email, url, abbreviation.
      return [self.add_pos(token, 'SYM')]

    ret = []
      
    if self.cls_dict.get(token.form.lower(), None): #word from closed class
      poss = self.cls_dict[token.form.lower()]
      for pos in poss:
        tag, ind = self.conv_dict.get(pos,(pos,0))
        lemm = token.form.lower()[:len(token.form) - ind]
        ret.append(self.add_pos(token, pos, tag, lemm))
      return ret
      
    if token.is_capital() and not new_sent: #If this word definetely proper
      if token.form.endswith('on'):
        ret.append(self.add_pos(token, 'PROPN', 'PROPSA', token.form[:-1]))
      ret.append(self.add_pos(token, 'PROPN', 'PROPSN'))
      
    if token.is_foreign(): #Don't parse foreign word by ending.
      return ret+[self.add_pos(token, 'X')]
      
    for fin in self.fin_dict.keys():
      if token.form.endswith(fin):
        tag = self.fin_dict[fin]
        pos, ind = self.conv_dict.get(tag,(tag,0))
        lemm = token.form.lower()[:len(token.form) - ind]
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
    fin = token.form[len(token.lemma):]
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
      lemm = token.form.lower()
    ret.lemma = lemm
    ret.upos = pos
    ret.xpos = tag
    return ret
    
    
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

  
def main():
  """Main function Loop, containing every step"""
  args = sys.argv[1:]
  pipeline = args[:]

  parser = MorfParser()
  while len(pipeline):

    source = ilo.get_source(pipeline.pop())
    out = ilo.get_out(source)

    if ilo.is_raw(source):
      print('Cxi programo laboras nur kun prilaborita teksto en CONLL-formato')
      quit()


    con = Conll(id=os.path.splitext(os.path.basename(source))[0])
    con.load_from_file(source)

    for sent in con.sentaro:
      parser.parse(sent)
      print(sent)

    con.update_sent_id()
    con.update_text()

    con.exportu(out)
      

if __name__=='__main__':
  main()
