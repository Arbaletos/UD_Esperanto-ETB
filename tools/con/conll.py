class Conll:
  """Full Conll representation of a document."""

  def __init__(self, id=None):
    self.id = id
    self.formal = True
    self.sentaro = []
    
  def load_from_file(self, fn):
    with open(fn, 'r') as f:
      self.exportu(f.read())
    
  def importu(self, text):
    '''
      Por esti sukcese eksportita, frazoj en via teksto devas esti divigitaj.
      Exportas conll el .con file.
    '''
    self.sentaro = [Sent(i, strings) for i, strings in enumerate(text.split('\n\n'))]
    
  def exportu(self, fn):
    with open(fn, 'w') as f:
      f.write(str(self))
    
  def __str__(self):
    '''
      spaces=True, ids=True, sent_tekst=True
    ''' 
    return ''.join([str(sent) for sent in self.sentaro])
    
  def update_sent_id(self):
    for i in range(len(self.sentaro)):
      self.sentaro[i].update_sent_id(str(i),self.id)
      
  def update_text(self):
    for s in self.sentaro:
      s.update_text()
      
  def add(self, sent):
    if type(sent) is Sent:
      self.sentaro.append(sent)
    else:
      self.sentaro.append(Sent(len(self.sentaro), sent))
     
  

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
          self.tokens.append(Token(*cols))
          
  def add(self, token):
    self.tokens.append(token)
        
  def __str__(self):
    ret = []
    for key in sorted(self.pars.keys()):
      ret.append('# {} = {}\n'.format(key, self.pars[key]))
    for tok in self.tokens:
      ret.append(str(tok)+'\n')
    ret.append('\n')
    return ''.join(ret)
    
  def update_sent_id(self, sent_id, text_id):
    self.pars['sent_id'] = text_id+'_'+sent_id
    
  def update_text(self):
    if len(self.tokens) == 0:
      return
    if self.is_formal():
      self.pars['text'] = ''.join([t.to_sent() for t in self.tokens])
    else:
      self.pars['text'] = ''
      id_0 = self.tokens[0].id
      for t in self.tokens:
          if t.id == id_0:
              id_0 += 1
              self.pars['text'] += t.to_sent()

  def is_formal(self):
    ids = [t.id for t in self.tokens]
    if len(set(ids)) < len(ids):
      return False
    return True
    
    
class Token:
  """Token class, containing all gramemes."""
  
  def __init__(self, cur_id='0', word='_', lemma='_', upos='X', xpos='_',
               feats='_', head='_', deprel='_', deps='_', misc='SpaceAfter=Yes'):
    self.id = cur_id
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
    return '\t'.join(str(x) for x in [self.id, self.word,
        self.lemma, self.upos, self.xpos, self.feats,
        self.head, self.deprel, self.deps, self.misc])
    
  def space_after(self):
    return self.misc.get('SpaceAfter', True)
  
  def to_sent(self):
    space = self.misc.get('SpaceAfter', True)
    if space:
      return self.word+' '
    return self.word

  def is_digit(self):
    return self.word.isdigit()

  def is_alpha(self):
    return self.word.isalpha()

  def is_punct(self):
    return self.word in ['.', ',', '...', '?', '!', '"', "'", ':', ';', '`', '(', ')']

  def is_symb(self):
    #necesas aldoni regexpojn!
    return not self.is_alpha() and not self.is_digit() and not self.is_punct()

  def is_capital(self):
    return self.word.istitle()

  def is_foreign(self):
    for_let = ['q','x','w','y']
    for let in for_let:
      if let in self.word:
        return True
    return False

  def add_misc(self, misc):
    self.misc.update(misc)

  def set_misc(self, misc):
    self.misc = ConllDict(misc)

  def add_feats(self, feats):
    self.feats.update(feats)

  def set_feats(self, feats):
    self.feats = ConllDict(feats)


class ConllDict:
  '''Dict incapsulation, that can be easily transformed and edited in CONLL
  string form.'''
  
  def __init__(self, data=None):


    if type(data) is str:
      self.dict = self.str_to_dict(data)
    elif type(data) is dict:
      self.dict = data
    else:
      self.dict = {}
      
      
  def get(self, k, d):
    try:
      return self.dict[k]
    except:
      return d
            
  def __getitem__(self, key):
    return self.dict[key]

  def __setitem__(self, key, value):
    self.dict[key] = value

  def update(self, nova):
      nova = ConllDict(nova)
      self.dict.update(nova.dict)
      
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
    '''returns True instead of 'Yes' and False instead of 'No'''
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
  if linearo[-1] == '':
      linearo = linearo[:-1]
  for i in range(1,len(linearo)):
    line = linearo[i]
    pre_line = linearo[i-1]
    if (line.startswith('1\t') or line.startswith('1-')) and len(pre_line) and pre_line[0] not in('#',' '):
      linearo[i-1] +='\n'
  return '\n'.join(linearo)
                
