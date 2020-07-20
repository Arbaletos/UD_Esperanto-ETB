from conll.conll import Token
from morf import kombiki, sent_split, Parser

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
    
  def test_token(case, form, space, isdigit, isalpha, ispunct, issymb):
    token = Token(form=form, misc={'SpaceAfter':space}) 
    case = 'Token '+str(case)
    ass(case, form, token.form, 'word')
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
    n_words = [token.form for token in n_tokens]
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