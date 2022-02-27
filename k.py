from logging import basicConfig, getLogger, CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
from env3 import Env3
from kindlelist import KindleList
import sys
import argparse
from calibrex import Calibrex
import json


def cmd_get(inst, target_name, target):
  response = inst.get_gss('purchase')
  fname = "get.json"
  content = json.dumps(response, separators=(',', ':'), sort_keys=True, indent=4)
  with open(fname, mode='w', encoding='utf-8') as f:
    f.write(content)

def cmd_append(inst, target_name, target):
  nary = []
  inst.db2gss_append('purchase')

def cmd_update(inst, target_name, target):
  db_fname = target.get_latest_db_fname()
  target.set_db_fname( db_fname )
  #inst = Calibrex(target, CMD)
  nary = []
  ret = self.src2db('book', nary)
  #self.db2gss_update('book')
  listx = []
  ret = self.get_id_from_db('book', listx)
  dict = { x[1]:x[0] for x in listx }
  nary_purchase = inst.dictarray_for_purchase(nary, dict)
  #self.dictarray2db('purchase', nary_purchase)
  nary_purchase = [ it for it in nary_purchase if it.get('purchase_date', None) != None ]
  inst.dictarray2db('purchase', nary_purchase)
  inst.db2gss_update('purchase', nary_purchase)


def cmd_batchUpdate(inst, target_name, target):
  print('appbase.py | cmd_batchUpdate')
  sheetname = 'sheet10'
  #exit(0)
  inst.db2gss_batchUpdate('purchase', sheetname)


def cmd_batchUpdate2(inst, target_name, target):
  print('appbase.py | cmd_batchUpdate2')
  #exit(0)
  inst.db2gss_batchUpdate2('purchase')

def db_process(env, target_name, cmd):
  if not target_name in env.d:
    logger.debug("{} is not in env.d".format(target_name))
    return None
  gcp = env.d['gcp']
  target = env.d[target_name]
  klass = env.d['klass'][target_name]
  inst = klass(target, gcp, cmd)
  if cmd == 'get':
    cmd_get(inst, target_name, target)
  elif cmd == 'create':
    cmd_create(inst, target_name, target)
  elif cmd == 'update':
    cmd_update(inst, target_name, target)
  elif cmd == 'batchupdate':
    print('k.py | batchupdate')
    #exit(0)
    cmd_batchUpdate(inst, target_name, target)
  elif cmd == 'batchupdate2':
    print('k.py | batchupdate2')
    #exit(0)
    cmd_batchUpdate2(inst, target_name, target)
  elif cmd == 'append':
    cmd_append(inst, target_name, target)
  elif cmd == 'json':
    fname = "get.json"
    with open(fname, mode='r', encoding='utf-8') as f:
      content = f.read()
    response = json.loads(content)
    list = response['sheets']
    list2 = [ it['data'] for it in list]
    #print( list2[0] )
    list3 = [ x['rowData'] for x in list2[0]]
    #print(list3[0])
    x = json.dumps(list3, separators=(',', ':'), sort_keys=True, indent=4)
    print(x)
    '''
    for x in list2:
      print(x)
      print('')
    '''

  #elif cmd == 'append':
  #  inst.cmd_update2(target_name, target, gcp)
  else:
    logger.error("unknown command: {}".format(cmd))
    sys.exit(1)
  inst.db_close()

# basicConfig(level=CRITICAL)
# basicConfig(level=ERROR)
# basicConfig(level=WARNING)
#basicConfig(level=INFO)
basicConfig(level=DEBUG)  #デバッグ時にアンコメントしよ
# basicConfig(level=NOTSET)
logger = getLogger(__name__)
logger.debug('main using debug. start running')
logger.debug('main finished running')

parser = argparse.ArgumentParser()
parser.add_argument('target', help='target help')
parser.add_argument('cmd', help='cmd help')
args = parser.parse_args(sys.argv[1:])
#logger.debug("--")
TARGET = args.target.lower()
CMD = args.cmd.lower()
#exit()

env3 = Env3()
db_process(env3, TARGET, CMD)
