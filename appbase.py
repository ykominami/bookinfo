from logging import basicConfig, getLogger, DEBUG
import csv
from appdb import AppDb
from util import Util
import json

from googleapiclientx import GoogleApiClientx
from credential import Credential

class AppBase:
  def __init__(self, env, env_gcp, cmd):
    self.logger = getLogger(__name__)
    self.logger.debug('using debug. start running')
    self.logger.debug('finished running')

    self.env = env
    self.cmd = cmd
    db = self.env.d['db']
    self.appdb = AppDb(
      self.cmd,
      db['db_file'],
      self.env,
    )
    self.encoding = db['encoding']
    self.newline = db['newline']
    self.table_env = {}
    self.credential = Credential(env_gcp)
    #self.credential.try_prepare_creds()

  def dictarray2db(self, key, nary):
    Util.escape_single_quote_all(nary, self.env.d[key]['text_fields'])
    #print("={}".format(key))
    #print(nary)
    #print("len={}".format(len(nary)))
    ret = self.appdb.insert_unique_record_all_and_commit(key, nary)
    return ret

  def create_table(self, key):
    #self.logger.debug("KindleList create_table")
    #self.appdb.create_table(key)
    self.appdb.create_table_and_commit(key)

  def db_close(self):
    #self.logger.debug("KindleList db_close")
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

  def db2gss_batchUpdate2(self, key, clear_flag=False):
    print('appbase.py | db2gss_batchUpdate2')
    #exit(0)
    listx = []
    requests = []
    ret = self.appdb.select_all_as_dict(key, listx)
    if ret and len(listx) > 0:
      print("db2gss_batchUpdate")
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
        print(body)
        print("====")
        #gac.upload2gss_append_with_body(body)
        gac.upload2gss_batchUpdate_with_body(body, clear_flag)

  def db2gss_batchUpdate(self, key, sheetname, clear_flag=False):
    print('appbase.py | db2gss_batchUpdate')
    #exit(0)
    listx = []
    ret = self.appdb.select_all_as_dict(key, listx)
    if ret and len(listx) > 0:
      print("db2gss_batchUpdate")
      gac = self.get_googleapiclientx(key)
      if gac:
        requests=[]
        requests.append({
            'addSheet':{
                "properties":{
                    "title": sheetname,
                    "index": "0",
                    }

                }
            })
        body={'requests':requests}
        gac.upload2gss_batchUpdate_with_body(body, clear_flag)

  def db2gss_update(self, key, data, clear_flag=False):
    print('appbase.py | db2gss_update_0')
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

  def db2gss_update_0(self, key, data, clear_flag=False):
    print('appbase.py | db2gss_update_0')
    #exit(0)
    listx = []
    ret = self.appdb.select_all_as_dict(key, listx)
    if ret and len(listx) > 0:
      print("db2gss_batchUpdate")
      gac = self.get_googleapiclientx(key)
      if gac:
        #range_ = 'sheet1'+"!A1:B10"
        table = self.env.d[key]
        range_ = table['RANGE_NAME']
        v={}
        v['range']=range_
        v['majorDimension']="ROWS"
        v['values']=[
        [1,  2, 4],
        [3,  4],
        [4,  5],
        [5,  6],
        [6,  7],
        [7,  8],
        [8,  9],
        [10, 11],
        [12, 13],
        ['test', 'スプレッドシートのテストですよ'],
        ]
        value_input_option = 'USER_ENTERED'
        insert_data_option = 'OVERWRITE'
        gac.upload2gss_update_with_body(v, value_input_option, insert_data_option, clear_flag)

  def get_id_from_db(self, key, nary):
    ret = self.appdb.select_all(key, nary, self.env.d[key]['id_related_columns'])
    return ret

  def dictarray_for_purchase(self, nary, dict):
    return [self.make_purchase_table_record(item, dict) for item in nary]

  def dictarray_for_progress(self, nary, dict):
    return [self.make_progress_table_record(item, dict) for item in nary]

  def src2db(self, table_name):
    raise NotImplementedError('not implement src2db')

  def cmd_create(self, target_name, target):
    self.logger.debug("create table {}".format(target_name))
    db_fname = target.get_new_db_fname()
    self.logger.debug(db_fname)
    self.logger.debug("------ START")
    target.set_db_fname( db_fname )
    self.create_table('book')
    self.create_table('purchase')
    self.create_table('progress')

    self.logger.debug("------ END")

  def cmd_update(self, target_name, target):
    self.logger.debug("update table {}".format(target_name))
    db_fname = target.get_latest_db_fname()
    self.logger.debug(db_fname)
    self.logger.debug("------")
    target.set_db_fname( db_fname )
    #inst = Calibrex(target, CMD)
    nary = []
    ret = self.src2db('book', nary)
    self.db2gss('book')
    listx = []
    ret = self.get_id_from_db('book', listx)
    dict = { x[1]:x[0] for x in listx }
    nary_purchase = self.dictarray_for_purchase(nary, dict)
    self.dictarray2db('purchase', nary_purchase)
    nary_purchase = [ it for it in nary_purchase if it.get('purchase_date', None) != None ]
    self.dictarray2db('purchase', nary_purchase)
    self.db2gss_update('purchase')


  def get_gss(self, key):
    print("get_gss")
    response = None
    #self.logger.debug(list)
    gac = self.get_googleapiclientx(key)
    if gac:
      range_val = 'Sheet10!A1:B10'

      #gac.upload2gss_append_with_body(body)
      ranges = [range_val]
      include_grid_data = True
      response = gac.gss_get(ranges, include_grid_data)
      #print(list2)
      #gac.upload2gss( listx2 )
    return response
