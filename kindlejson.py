from logging import basicConfig, getLogger, DEBUG
import csv
import sys
import os
import datetime
from appbase import AppBase
from appdb import AppDb
from util import Util

import json
from pathlib import PurePath, Path
import re

class KindleJSON(AppBase):
  def __init__(self, env, env_gcp, cmd):
    self.logger = getLogger(__name__)
    self.logger.debug('using debug. start running')
    self.logger.debug('finished running')

    self.json_file_list = []

    home = os.environ['HOME']
    self.json_parent_path = Path(home, "dotfiles", "kindle")

    super().__init__(env, env_gcp, cmd)

  def create_table(self, key):
    self.logger.debug("KindleList create_table")
    self.appdb.create_table_and_commit(key)

  def db_close(self):
    self.logger.debug("KindleList db_close")
    self.appdb.close()

  def src2db(self, key, nary):
    nary.extend(self.json2dictarray(key))
    ret = self.dictarray2db(key, nary)
    return ret

  def get_json_file_list(self):
    item_list = list(self.json_parent_path.glob("*"))
    for item in item_list:
      if item.is_dir() == True:
        if re.match(r'^[0-9]+$', item.name) != None:
          self.json_file_list = self.json_file_list + list(item.glob("**/*"))

  def json2dictarray(self, key):
    nary = []
    xdict = {}
    self.get_json_file_list()
    for n in self.json_file_list:
      with Path(n).open( encoding='utf_8' ) as f:
        dict = json.load(f)
        itemlist = dict['itemsList']
        #xdict = xdict | { item['asin']: item for item in itemlist }
        nary = nary + itemlist

    return nary

  def make_purchase_table_record(self, item, dict):
    if item.get('purchase_date', None) != None:
      dt = datetime.datetime.strptime( item['purchase_date'], "%Y-%m-%dT%H:%M:%S+0000" )
      year_str = "%04d" % dt.year
      month_str = "%02d" % dt.month
      day_str = "%02d" % dt.day
      year_month_str = "%s%s" % (year_str, month_str)
      year_month_day_str = "%s%s%s" % (year_str, month_str, day_str)
      ret_dict = {'asin':item['asin'], 'ext_id':dict[ item['asin'] ], 'purchase_date':item['purchase_date'], 
      'year':year_str, 'month':month_str, 'day':day_str, 'year_month':year_month_str,
      'year_month_day':year_month_day_str}
    else:
      ret_dict = None

    return ret_dict

  def make_progress_table_record(self, item, dict):
    if item.get('progress_date', None) != None:
      dt = datetime.datetime.strptime( item['progress_date'], "%Y-%m-%dT%H:%M:%S+0000" )
      year_str = "%04d" % dt.year
      month_str = "%02d" % dt.month
      day_str = "%02d" % dt.day
      year_month_str = "%s%s" % (year_str, month_str)
      year_month_day_str = "%s%s%s" % (year_str, month_str, day_str)
      ret_dict = {'asin':item['asin'], 'ext_id':dict[ item['asin'] ], 'progress_date':item['progress_date'], 
      'year':year_str, 'month':month_str, 'day':day_str, 'year_month':year_month_str,
      'year_month_day':year_month_day_str}
    else:
      ret_dict = None

    return ret_dict
