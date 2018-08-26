class Conll:
  """Full Conll representation of a document."""

  def __init__(self, text, id=''):
    self.sentaro = [Sent(strings) for strings in text.split('\n\n')]
    self.id = id
    
  def __str__(self):
    return ''.join([str(sent) for sent in self.sentaro])
    
  def update_sent_id(self):
    for i in range(len(self.sentaro)):
      self.sentaro[i].update_sent_id(str(i),self.id)
      
  def update_text(self):
    for s in self.sentaro:
      s.update_text()
  

  
class Sent:
  """The conll sentence, contains table, id and coolstory"""
  
  def __init__(self,strings):  
    self.tokens = []
    self.pars = {}
    tokens = strings.split('\n')
    for tok in tokens:
      if tok.strip().startswith('#'):
        pars = tok.strip()[1:].split('=')
        if len(pars)>=2:
          self.pars[pars[0].strip()] = pars[1].strip()
      else:
        cols = tok.split('\t')
        self.tokens.append(Token(cols))
        
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
  
  def __init__(self, cols):
    if len(cols) < 10:
      cols = cols+['_']*(10-len(cols))
    self.id = cols[0]
    self.word = cols[1]
    self.feat_dict = str_to_dict(cols[5]) #feats can be dict
    self.misc_dict = str_to_dict(cols[9]) #misc can be dict
    if cols[3]=='_': #Kostyl for TAG(can't be underscore)
      cols[3] = 'X'
    self.cols = cols
    
  def __str__(self):
    return '\t'.join(self.cols)
    
  def to_sent(self):
    space = self.misc_dict.get('SpaceAfter', 'Yes')
    if space=='Yes':
      return self.cols[1]+' '
    return self.cols[1]
 
          
def str_to_dict(in_str):
  ret = {}
  if in_str=='_':
    return ret
  keys = in_str.split('|')
  return {k.split('=')[0]:k.split('=')[1] for k in keys}
  

def insert_spaces(text):
  linearo = text.split('\n')
  for i in range(1,len(linearo)):
    line = linearo[i]
    pre_line = linearo[i-1]
    if (line.startswith('1\t') or line.startswith('1-')) and len(pre_line) and pre_line[0] not in('#',' '):
      linearo[i-1] +='\n'
  return '\n'.join(linearo)
                