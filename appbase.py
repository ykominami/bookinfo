from logging import basicConfig, getLogger, DEBUG
import csv
from appdb import AppDb
from util import Util
import json

from googleapiclientx import GoogleApiClientx
from credential import Credential

class AppBase:
  def __init__(self, specific_env, env_gcp, cmd):
    self.logger = getLogger(__name__)
    self.logger.debug('using debug. start running')
    self.logger.debug('finished running')

    self.specific_env = specific_env
    self.cmd = cmd
    db = self.specific_env.target.d['db']
    #print("AppBase __init__ db={}".format(db))
    self.appdb = AppDb(
      self.cmd,
      db['db_file'],
      self.specific_env,
    )
    self.encoding = db['encoding']
    self.newline = db['newline']
    self.table_env = {}
    self.credential = Credential(env_gcp)

  def dictarray2db(self, key, nary):
    text_fields = []
    if 'text_fields' in self.env.d[key].keys():
      if self.env.d[key]['text_fields'] is not None:
        text_fields = self.env.d[key]['text_fields']

    array_to_string_fields = []
    if 'array_to_string_fields' in self.env.d[key].keys():
      if self.env.d[key]['array_to_string_fields'] is not None:
        array_to_string_fields = self.env.d[key]['array_to_string_fields']

    Util.escape_single_quote_all(nary, text_fields, array_to_string_fields)

    boolean_fields = []
    if 'boolean_fields' in self.env.d[key].keys():
      if self.env.d[key]['boolean_fields'] is not None:
        boolean_fields = self.env.d[key]['boolean_fields']

    self.appdb.convert_boolean_to_integer(nary, boolean_fields)

    ret = self.appdb.insert_unique_record_all_and_commit(key, nary)

    return ret

  def create_table(self, key):
    self.appdb.create_table_and_commit(key)

  def db_close(self):
    self.appdb.close()

  def csv2dict(self):
    db = self.env.d['db']
    ret = False
    with open(db['incsvfile'], encoding=self.encoding, newline=self.newline) as f:
      r = csv.DictReader(f)
      content = [row for row in r if row['id'] != '']

    return content

  def get_googleapiclientx(self, key):
    gac = self.table_env.get(key, None)
    if not gac:
      table_env = self.env.d[key]
      gac = GoogleApiClientx(table_env, self.credential)
      self.table_env[key] = gac
    return gac

  def db2gss_append(self, key, clear_flag=False):
    listx = []
    ret = self.appdb.select_all_as_dict(key, listx)
    return ret

  def db2gss_batchUpdate2(self, key, clear_flag=False):
    self.logger.debug('appbase.py | db2gss_batchUpdate2')
    #exit(0)
    listx = []
    requests = []
    ret = self.appdb.select_all_as_dict(key, listx)
    if ret and len(listx) > 0:
      self.logger.debug("db2gss_batchUpdate")
      gac = self.get_googleapiclientx(key)
      if gac:
        requests.append({
            "updateBorders":{
                "range": {
                    "sheetId": self.env.d[key]['SPREADSHEET_ID'],
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 2,
                    },
                "bottom": {
                    "style": "SOLID",
                    "width": "1",
                    "color": { "red": 0, "green":0, "blue":0 },
                    },
                },
            })
        requests.append({
          "repeatCell": {
              "range": {
                  "sheetId": int(self.env.d[key]['SPREADSHEET_ID']),
                  "startRowIndex": 0,
                  "endRowIndex": 1,
                  "startColumnIndex": 0,
                  "endColumnIndex": 2,
              },
              "cell": {
                  "userEnteredFormat": {
                      "horizontalAlignment" : "LEFT",
                      "textFormat": {
                          "fontSize": 11,
                          "bold": True,
                          "foregroundColor": {
                              "red": 1.0,
                              },
                          }
                      }
                  },
              "fields": "userEnteredFormat(textFormat,horizontalAlignment)"
              },
          })

        body = { 'requests': requests }
        gac.upload2gss_batchUpdate_with_body(body, clear_flag)


  def db2gss_update(self, key, *, clear_flag=False):
    self.logger.debug('appbase.py | db2gss_update')
    listx = []
    ret = self.appdb.select_all_as_dict(key, listx)
    if ret and len(listx) > 0:
      gac = self.get_googleapiclientx(key)
      if gac:
        table = self.env.d[key]
        range_ = table['RANGE_NAME']
        value_input_option = 'USER_ENTERED'
        insert_data_option = 'OVERWRITE'
        gac.upload2gss_update_with_body(listx, value_input_option, insert_data_option, clear_flag)

  def get_id_from_db(self, key, nary):
    ret = self.appdb.select_all(key, nary, self.env.d[key]['id_related_columns'])
    return ret

  def dictarray_for_purchase(self, nary, dict):
    return [self.make_purchase_table_record(item, dict) for item in nary]

  def dictarray_for_progress(self, nary, dict):
    return [self.make_progress_table_record(item, dict) for item in nary]

  def src2db(self, table_name):
    raise NotImplementedError('not implement src2db')

  def get_gss(self, key, *, ranges=None, value_render_option='FORMATTED_VALUE', date_time_render_option='FORMATTED_STRING'):
    self.logger.debug("get_gss")
    response = {}
    gac = self.get_googleapiclientx(key)
    if gac:
      if ranges == None:
        range_val = 'Sheet1!A1:B10'
        ranges = range_val
      self.logger.debug("ranges={} value_render_option={} date_time_render_option={}".format(ranges, value_render_option, date_time_render_option))
      response = gac.gss_get(ranges, value_render_option=value_render_option, date_time_render_option=date_time_render_option)
      #response = {}
    return response
