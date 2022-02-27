class Util:
  @classmethod
  def escape_single_quote(cls, s):
    return s.replace("'", "\'\'")

  @classmethod
  def escape_single_quote_all(cls, nary, text_fields):
    for dict in nary:
      for h in text_fields:
        '''
        #print(dict)
        #print("type(dict)={}".format(type(dict)))
        #print(h)
        #print(type(h))
        #print(text_fields)
        '''
        if dict[h] != None:
          dict[h] = cls.escape_single_quote(dict[h])
