class Conll:
  """Full Conll representation of a document."""

  def __init__(self, id=None):
    self.id = id
    self.formal = True
    self.sentaro = []
    self.col_names = ['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS', 'FEATS', 'HEAD', 'DEPREL', 'DEPS', 'MISC']
    
  def load_from_file(self, fn):
    with open(fn, 'r') as f:
      self.importu(f.read())

  def get_col_names(self):
    return self.col_names
    
  def importu(self, text):
    '''
      Por esti sukcese eksportita, frazoj en via teksto devas esti divigitaj.
      Exportas conll el .con file.
    '''
    self.sentaro = [Sent(strings) for strings in text.split('\n\n') if len(strings)]
    
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
  
  def get_size(self):
      return len(self.sentaro)

  def get_sent(self, sent_id):
      return self.sentaro[sent_id]

  def kunigi_sentoj(self, sent_id):
    """Kunigas la sent_id sento kun la sekva"""
    self.sentaro[sent_id].kunigi(self.sentaro[sent_id+1])
    self.sentaro = self.sentaro[:sent_id+1] + self.sentaro[sent_id+2:]
    self.update_sent_id()

  def disigi_sentoj(self, sent_id, i):
    """Faras du sentoj el unu"""
    novasento = self.sentaro[sent_id].disigi(i)
    if novasento is None:
      return
    self.sentaro.insert(sent_id+1, novasento)
    self.update_sent_id()
     
  

class Sent:
  """The conll sentence, contains tokens, id and coolstory"""
  
  def __init__(self, strings=None):  
    self.tokens = []
    self.pars =  {}
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
  
  def insert_token(self, token, i, id_shift=False):
    """inserts token into tesktaro, and shifts all ids post new one"""
    self.tokens.insert(i, token)
    if not id_shift:
      return
    for t in self.tokens[i+1:]:
      if t.id >= token.id:
          t.id += 1

  def delete_token(self, i, id_shift=False):
    """deletes token from sentaro and decreases all token's id post it if id_shift"""
    last_id = self.tokens[i].id
    self.tokens = self.tokens[:i]+self.tokens[i+1:]
    if not id_shift:
      return
    for t in self.tokens[i:]:
      if t.id > last_id:
          t.id -= 1

  def kunigi(self, sent):
    t0 = 0 if not len(self.tokens) else self.tokens[-1].id
    for t in sent.tokens:
      t.id += t0
    self.tokens = self.tokens + sent.tokens
    self.update_text()

  def disigi(self, i):
    """Splits this sent by i id kaj returns new sent."""
    if i>=len(self.tokens):
        return None
    new_sent = Sent()
    for t in self.tokens[i:]:
        t.id -= self.tokens[i-1].id
        new_sent.add(t)
    self.tokens = self.tokens[:i]
    new_sent.update_text()
    self.update_text()
    return new_sent
        
  def __str__(self):
    ret = []
    for key in sorted(self.pars.keys()):
      ret.append('# {} = {}\n'.format(key, self.pars[key]))
    for tok in self.tokens:
      ret.append(str(tok)+'\n')
    ret.append('\n')
    return ''.join(ret)

  def get_values(self):
    "Returns sent data as an 2-d list"
    return [str(t).split('\t') for t in self.tokens]

  def get_sent_id(self):
    return self.pars.get('sent_id', '')

  def get_text(self):
    return self.pars.get('text', '')
    
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
  
  def __init__(self, cur_id='0', form='_', lemma='_', upos='X', xpos='_',
               feats='_', head='_', deprel='_', deps='_', misc='SpaceAfter=Yes'):
    self.id = int(cur_id)
    self.form = form 
    self.lemma = lemma
    self.upos = upos
    self.xpos = xpos
    self.feats = ConllDict(feats) #feats can be dict
    self.head = head
    self.deprel = deprel
    self.deps = deps
    self.misc = ConllDict(misc) #misc can be dict

    self.field_list = ['id', 'form', 'lemma', 'upos', 'xpos',
                       'feats', 'head', 'deprel', 'deps', 'misc']

  def __str__(self):
    return '\t'.join([str(self[x]) for x in self.field_list])


  def __getitem__(self, key):
    if key in range(10):
        key = self.field_list[key]
    if key in self.field_list:
      return self.__dict__[key]

  def __setitem__(self, key, val):
    if key in range(10):
      key = self.field_list[key]
    if key in self.field_list:
      self.__dict__[key] = val

  def space_after(self):
    return self.misc.get('SpaceAfter', True)
  
  def to_sent(self):
    space = self.misc.get('SpaceAfter', True)
    if space:
      return self.form+' '
    return self.form

  def is_digit(self):
    return self.form.isdigit()

  def is_alpha(self):
    return self.form.isalpha()

  def is_punct(self):
    return self.form in ['.', ',', '...', '?', '!', '"', "'", ':', ';', '`', '(', ')']

  def is_symb(self):
    #necesas aldoni regexpojn!
    return not self.is_alpha() and not self.is_digit() and not self.is_punct()

  def is_capital(self):
    return self.form.istitle()

  def is_foreign(self):
    for_let = ['q','x','w','y']
    for let in for_let:
      if let in self.form:
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
                
