from logging import basicConfig, getLogger, DEBUG
import xml.etree.ElementTree as ET
import sys
import os
from appbase import AppBase
from appdb import AppDb
from util import Util

class Calibrex(AppBase):
  def __init__(self, env, env_gcp, cmd):
    self.logger = getLogger(__name__)
    self.logger.debug('Calibrex using debug. start running')
    self.logger.debug('Calibrex finished running')

    super().__init__(env, env_gcp, cmd)

  '''
  def test_csv2db(self):
    val0 = "O'm a tes't strin'g"
    s = self.escape_single_quote(val0)
    self.appdb.test_insert(s)
  '''

  def csv2dict0(self):
    ret = False
    with open(self.incsvfile, encoding=self.encoding, newline=self.newline) as f:
    #with open(self.incsvfile, encoding="utf_8_sig", newline=self.newline) as f:
      r = csv.DictReader(f)
      # content = [row for row in r if row['ASIN'] != '' and self.appdb.select_none(row['ASIN']) is True]
      content = [row for row in r if row['id'] != '']

    return content

  def add_item(self, dict):
    dict['xxid'] = "-".join(map(lambda k: dict[k], ['isbn','id','uuid']))
    return dict

  def csv2dictarray(self):
    ret = False
    content = super().csv2dict()
    contentx = [ self.add_item(dict) for dict in content ]
    return contentx

  def make_purchase_table_record(self, item, dict):
      ret_dict = {'xxid':item['xxid'], 'ext_id':dict[ item['xxid'] ], 'purchase_date':None,
      'year':None, 'month':None, 'day':None, 'year_month':None,
      'year_month_day':None}

      return ret_dict

  def make_progress_table_record(self, item, dict):
      ret_dict = {'xxid':item['xxid'], 'ext_id':dict[ item['xxid'] ], 'progress_date':None,
      'year':None, 'month':None, 'day':None, 'year_month':None,
      'year_month_day':None}

      return ret_dict

  def src2db(self, key, nary):
    nary2 = nary + self.csv2dictarray()
    ret = self.dictarray2db(key, nary2)
    return ret

  def cmd_update(self, target_name,  target, gcp):
    self.logger.debug("update table {}".format(target_name))
    db_fname = target.get_latest_db_fname()
    self.logger.debug(db_fname)
    self.logger.debug("------")
    target.set_db_fname( db_fname )
    #inst = Calibrex(target, CMD)
    nary = []
    ret = self.src2db('book', nary)
    self.db2gss('book', gcp)
    list = []
    ret = self.get_id_from_db('book', list)
    dict = { x[1]:x[0] for x in list }
    nary_purchase = self.dictarray_for_purchase(nary, dict)
    self.dictarray2db('purchase', nary_purchase)
    nary_purchase = [ it for it in nary_purchase if it.get('purchase_date', None) != None ]
    self.dictarray2db('purchase', nary_purchase)
    self.db2gss_update('purchase', gcp)

    nary_progress = self.dictarray_for_progress(nary, dict)
    nary_progress = [ it for it in nary_progress if it.get('progress_date', None) != None ]
    self.dictarray2db('progress', nary_progress)
    self.db2gss_update('progress', gcp)
