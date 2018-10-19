class Conll:
  """Full Conll representation of a document."""

  def __init__(self, id=None):
    self.id = id
    self.formal = True
    
  def exportu(self, text):
  '''
  Por esti sukcese eksportita, frazoj en via teksto devas esti divigitaj.
  '''
    self.sentaro = [Sent(strings) for strings in text.split('\n\n')]
    
  def importu(self, spaces=True, ids=True, sent_tekst=True):
    return str(self)
    
  def __str__(self):
    return ''.join([str(sent) for sent in self.sentaro])
    
  def update_sent_id(self):
    for i in range(len(self.sentaro)):
      self.sentaro[i].update_sent_id(str(i),self.id)
      
  def update_text(self):
    for s in self.sentaro:
      s.update_text()
  

class Sent:
  """The conll sentence, contains tokens, id and coolstory"""
  
  def __init__(self, id=None, strings=None):  
    self.tokens = []
    self.pars = {'id':id} if id is not None else {}
    if strings is not None:
      tokens = strings.split('\n')
      for tok in tokens:
        if tok.strip().startswith('#'):
          pars = tok.strip()[1:].split('=')
          if len(pars)>=2:
            self.pars[pars[0].strip()] = pars[1].strip()
        else:
          cols = tok.split('\t')
          self.tokens.append(Token(cols))
          
  def add(self, token):
    self.tokens.append(token)
        
  def __str__(self):
    ret = []
    for key in sorted(self.pars.keys()):
      ret.append(f'# {key} = {self.pars[key]}\n')
    for tok in self.tokens:
      ret.append(str(tok)+'\n')
    ret.append('\n')
    return ''.join(ret)
    
  def update_sent_id(self, sent_id, text_id):
    self.pars['sent_id'] = text_id+sent_id
    
  def update_text(self):
    self.pars['text'] = ''.join([t.to_sent() for t in self.tokens])
    
    
class Token:
  """Token class, containg all gramemes."""
  
  #def __init__(self, cols):
  def __init__(self, id='0', word='_', lemma='_', upos='X', xpos='_',
               feats='_', head='_', deprel='_', deps='_', misc='SpaceAfter=Yes')
    self.id = id
    self.word = word
    self.lemma = lemma
    self.upos = upos
    self.xpos = xpos
    self.feats = ConllDict(feats) #feats can be dict
    self.head = head
    self.deprel = deprel
    self.deps = deps
    self.misc = ConllDict(misc) #misc can be dict
  
  def __str__(self):
    return '\t'.join(self.cols)
  
  def to_sent(self):
    space = self.misc_dict.get('SpaceAfter', 'Yes')
    if space=='Yes':
      return self.word+' '
    return self.word
    

class ConllDict:
  '''Dict incapsulation, that can be easily transformed and edited in CONLL string form.'''
  
  def __init__(self, data=None):
    if type(data)=='str':
      self.data = self.str_to_dict(data)
    elif type(data)=='dict':
      self.dict = data
    else:
      self.dict = {}
            
  def __getitem__(self, key):
    return self.dict[key]

  def __setitem__(self, key, value):
    self.dict[key] = value
      
  def __str__(self):
    return '|'.join(['{}={}'.format(k, self.to_str(self.dict[k])) for k in sorted(self.dict)]) if len(self.dict) else '_'
    
  def to_str(self, arg):
  '''returns string from a par: Yes for True, No for False, str for str'''
  if arg==True:
    return 'Yes'
  if arg==False:
    return 'No'
  return str(arg)
  
  def to_bool(self,arg):
  '''returns True instead of 'Yes' and False instead of 'No''''
  if arg=='Yes':
    return True
  if arg=='No':
    return False
  return str(arg)
  
  def str_to_dict(self, in_str):
    ret = {}
    if in_str=='_':
      return ret
    keys = in_str.split('|')
    return {k.split('=')[0]:self.to_bool(k.split('=')[1]) for k in keys}
  

def insert_spaces(text):
  '''Add blank lines in conll before each sentence, if they are not here.'''
  linearo = text.split('\n')
  for i in range(1,len(linearo)):
    line = linearo[i]
    pre_line = linearo[i-1]
    if (line.startswith('1\t') or line.startswith('1-')) and len(pre_line) and pre_line[0] not in('#',' '):
      linearo[i-1] +='\n'
  return '\n'.join(linearo)
                