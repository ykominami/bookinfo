from logging import basicConfig, getLogger, DEBUG
import xml.etree.ElementTree as ET
import csv
import sys
import os
import datetime
from appbase import AppBase
from appdb import AppDb
from util import Util
class KindleList(AppBase):
  def __init__(self, env, env_gcp, cmd):
    self.logger = getLogger(__name__)
    self.logger.debug('KindleList using debug. start running')
    self.logger.debug('KindleList finished running')

    super().__init__(env, env_gcp, cmd)

  def create_table(self, key):
    self.logger.debug("KindleList create_table")
    self.appdb.create_table_and_commit(key)

  def db_close(self):
    self.logger.debug("KindleList db_close")
    self.appdb.close()

  def src2db(self, key, nary):
    nary.extend(self.xml2dictarray(key))
    ret = self.dictarray2db(key, nary)
    return ret

  def xml2dictarray(self, key):
    nary = []
    tree = ET.parse(self.env.d['db']['kindle_cache_file'])
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
      dict0 = { k: v for (k, v) in zip(self.env.d[key]['xml_headers'], ary)}
      nary.append(dict0)
    return nary

  def make_purchase_table_record(self, item, dict):
    if item.get('purchase_date', None) != None:
      dt = datetime.datetime.strptime( item['purchase_date'], "%Y-%m-%dT%H:%M:%S+0000" )
      year_str = "%04d" % dt.year
      month_str = "%02d" % dt.month
      day_str = "%02d" % dt.day
      year_month_str = "%s%s" % (year_str, month_str)
      year_month_day_str = "%s%s%s" % (year_str, month_str, day_str)
      ret_dict = {'ASIN':item['ASIN'], 'ext_id':dict[ item['ASIN'] ], 'purchase_date':item['purchase_date'], 
      'year':year_str, 'month':month_str, 'day':day_str, 'year_month':year_month_str, 
      'year_month_day':year_month_day_str}
    else:
      ret_dict = {'ASIN':item['ASIN'], 'ext_id':dict[ item['ASIN'] ], 'purchase_date':None, 
      'year':None, 'month':None, 'day':None, 'year_month':None, 
      'year_month_day':None}

    return ret_dict

  def make_progress_table_record(self, item, dict):
    if item.get('progress_date', None) != None:
      dt = datetime.datetime.strptime( item['progress_date'], "%Y-%m-%dT%H:%M:%S+0000" )
      year_str = "%04d" % dt.year
      month_str = "%02d" % dt.month
      day_str = "%02d" % dt.day
      year_month_str = "%s%s" % (year_str, month_str)
      year_month_day_str = "%s%s%s" % (year_str, month_str, day_str)
      ret_dict = {'ASIN':item['ASIN'], 'ext_id':dict[ item['ASIN'] ], 'progress_date':item['progress_date'], 
      'year':year_str, 'month':month_str, 'day':day_str, 'year_month':year_month_str, 
      'year_month_day':year_month_day_str}
    else:
      ret_dict = {'ASIN':item['ASIN'], 'ext_id':dict[ item['ASIN'] ], 'progress_date':None, 
      'year':None, 'month':None, 'day':None, 'year_month':None, 
      'year_month_day':None}

    return ret_dict
