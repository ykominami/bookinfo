import json

class Util:
  @classmethod
  def escape_single_quote(cls, s):
    ret_list = []
    ret_dict = {}
    x = type(s)
    if x == str:
      return s.replace("'", "\'\'")
    elif x == list:
      for i in s:
        ret_list = ret_list + [i.replace("'", "\'\'")]
      return ret_list
    elif x == dict:
      for k, v in s.items():
        ret_dict[k] = v.replace("'", "\'\'")
      return ret_dict
    else:
      return s

  @classmethod
  def escape_single_quote_all(cls, nary, text_fields, array_to_string_fields=[]):
    for dict in nary:
      for h in text_fields:
        if h in dict.keys():
          if dict[h] != None:
            dict[h] = cls.escape_single_quote(dict[h])
            if h in array_to_string_fields:
              dict[h] = ','.join(dict[h])
        else:
          raise

  @classmethod
  def save_as_file(cls, content, fname):
    with open(fname, mode='w', encoding='utf-8') as f:
      f.write(content)

  @classmethod
  def json2str(cls, response):
    content = json.dumps(response, separators=(',', ':'), sort_keys=True, indent=4)
    return content

  @classmethod
  def json2file(cls, response, fname):
    content = cls.json2str(response)
    Util.save_as_file(content, fname)
