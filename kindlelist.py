import xml.etree.ElementTree as ET
import csv
import sys
import os
from appdb import AppDb
from googleapiclientx import GoogleApiClientx

class KindleList:
  def __init__(self, env):
    self.env = env
    self.appdb = AppDb(self.env.db_file, self.env.table_name, self.env.table_def_stmt)
    self.appdb.ensure_connect()
    self.incsvfile = env.get_incsvfile()
    self.encoding = env.get_encoding()
    self.newline = env.get_newline()
    self.incsv_headers = env.get_incsv_headers()
    self.text_fields = ['title', 'authors', 'publishers']
    self.googleapiclientx = GoogleApiClientx(self.env)

  def escape_single_quote(self, s):
    return s.replace("'", "\'\'")

  def test_csv2db(self):
    val0 = "O'm a tes't strin'g"
    s = self.escape_single_quote(val0)
    #val = 'I\'\'m a test string'
    self.appdb.test_insert(s)

  def xml2dictarray(self):
    nary = []
    tree = ET.parse(self.env.get_kindle_cache_file())
    root = tree.getroot()

    for book_info in root[2]:
      ary = []
      for info in book_info:
        #authers publishers are nested
        if len(info) == 0:
          ary.append(info.text)
          '''
          rec = [info.text]
          print("rect={0}".format(rec))
          '''
        else:
          info_list = [ s.text for s in info ]
          s = ','.join(info_list)
          #print("info_list=", info_list)
          ary.append(s)
      dict0 = { k: v for (k, v) in zip(self.incsv_headers, ary)}
      print(dict0)
      nary.append(dict0)
    return nary

  def xml2dictarray_0(self):
    nary = []
    tree = ET.parse(self.env.get_kindle_cache_file())
    root = tree.getroot()

    for book_info in root[2]:
      for info in book_info:
        #authers publishers are nested
        if len(info) == 0:
          rec = [info.text]
        else:
          info_list = [ s.text for s in info ]
          rec.extend(info_list)
          #nary.append( { k: v for (k, v) in zip(self.incsv_headers, rec)} )
          print(self.incsv_headers)
          print(rec)
          #exit(0)
          dict0 = { k: v for (k, v) in zip(self.incsv_headers, rec)}
          print(dict0)
          exit(0)

    return nary

  def dictarray2db(self, nary):
    ret = False
    for cont in nary:
      dict0 = {}
      for h in self.text_fields:
        #dict0[h] = self.escape_single_quote(cont[h])
        if cont[h] != None:
          cont[h] = self.escape_single_quote(cont[h])
    ret = self.appdb.insert_all(nary)
    return ret

  def xml2db_with_dict(self):
    #exit(0)
    nary = self.xml2dictarray()
    content = [rows for rows in nary if self.xtest(rows, 'ASIN')]
    #exit(0)
    #print(content)
#    content = nary
    ret = self.dictarray2db(content)
    return ret

  def xtest(self, dictx, key):
    print(dictx) 
    ret0 = dictx[key] != ''
    ret1 = self.appdb.select_none(dictx[key]) is True
    ret = ret0 and ret1
    return ret

  def xml2db_bulk_with_dict(self):
    nary = self.xml2dictarray()
    ret = self.dictarray2db(nary)
    return ret

  def db2gss(self):
    list = []
    ret = self.appdb.select_all(list)
    if ret and len(list) > 0:
      #print(list)
      gac = GoogleApiClientx(self.env)
      gac.prepare_creds()
      gac.upload2gss(list)
'''

  def db2gss_0(self):
    list = []
    ret = self.appdb.select_all_as_dict(list)
#    print("ret={0}".format(ret))
#    print(list)
    if ret and len(list) > 0:
      gac = GoogleApiClientx()
      gac.prepare_creds()
      lists = [v for (k, v) in list]
      #
      #print( len(list) )
      #for row in list:
      #  print( type(row) )
'''

'''
  def csv2db_bulk_with_dict(self):
    ret = False
    with open(self.incsvfile, encoding=self.encoding, newline=self.newline) as f:
      r = csv.DictReader(f)
      content = [row for row in r]
      ret = dictarray2db(content)
    return ret

  def csv2db_with_dict(self):
    ret = False
    with open(self.incsvfile, encoding=self.encoding, newline=self.newline) as f:
      r = csv.DictReader(f)
      content = [row for row in r if row['ASIN'] != '' and self.appdb.select_none(row['ASIN']) is True]
      dictarray2db(content)

    return ret

  def csv2db(self):
    ret = False
    with open(self.incsvfile, encoding=self.encoding, newline=self.newline) as f:
      header = next(csv.reader(f))
      r = csv.reader(f)
      data = list(r)
      data = [row for row in r]

      for row in data:
        print(row[0])
        print(row[1])

    return ret

'''
