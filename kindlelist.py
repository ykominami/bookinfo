from logging import basicConfig, getLogger, DEBUG
import xml.etree.ElementTree as ET
import csv
import sys
import os
from appdb import AppDb
from googleapiclientx import GoogleApiClientx

class KindleList:
  def __init__(self, env, cmd):
    self.logger = getLogger(__name__)
    self.logger.debug('using debug. start running')
    self.logger.debug('finished running')

    self.env = env
    self.cmd = cmd
    self.appdb = AppDb(self.cmd, self.env.db_file, self.env.table_name, self.env.table_def_stmt)
    if self.cmd == 'UPDATE':
      self.incsvfile = env.incsvfile
      self.encoding = env.encoding
      self.newline = env.newline
      self.incsv_headers = env.incsv_headers
      self.text_fields = ['title', 'authors', 'publishers']
      self.googleapiclientx = GoogleApiClientx(self.env)

  def create_table(self):
    self.logger.debug("KindleList create_table")
    self.appdb.create_table()

  def db_close(self):
    self.logger.debug("KindleList db_close")
    self.appdb.close()

  def escape_single_quote(self, s):
    return s.replace("'", "\'\'")

  def test_csv2db(self):
    val0 = "O'm a tes't strin'g"
    s = self.escape_single_quote(val0)
    self.appdb.test_insert(s)

  def xml2dictarray(self):
    nary = []
    tree = ET.parse(self.env.kindle_cache_file)
    root = tree.getroot()

    for book_info in root[2]:
      ary = []
      for info in book_info:
        #authers publishers are nested
        if len(info) == 0:
          ary.append(info.text)
        else:
          info_list = [ s.text for s in info ]
          s = ','.join(info_list)
          #self.logger.debug("info_list=", info_list)
          ary.append(s)
      dict0 = { k: v for (k, v) in zip(self.incsv_headers, ary)}
      # self.logger.debug(dict0)
      nary.append(dict0)
    return nary

  def escape_single_quote_all(self, nary):
    for cont in nary:
      for h in self.text_fields:
        if cont[h] != None:
          cont[h] = self.escape_single_quote(cont[h])

  def dictarray2db(self, nary):
    self.escape_single_quote_all(nary)
    ret = self.appdb.insert_unique_record_all_and_commit(nary)
    return ret

  def dictarray2db_bulk(self, nary):
    self.escape_single_quote_all(nary)
    ret = self.appdb.insert_all_and_commit(nary)
    return ret

  def xml2db_with_dict(self):
    nary = self.xml2dictarray()
    content = [fields for fields in nary if fields['ASIN'] != None]
#    content_2 = [ content[0]]
    ret = self.dictarray2db(content)
#    ret = self.dictarray2db(content_2)
    return ret

  def xml2db_bulk_with_dict(self):
    nary = self.xml2dictarray()
    ret = self.dictarray2db_bulk(nary)
    return ret

  def db2gss(self):
    list = []
    ret = self.appdb.select_all(list)
    if ret and len(list) > 0:
      #self.logger.debug(list)
      gac = GoogleApiClientx(self.env)
      gac.prepare_creds()
      gac.upload2gss(list)
