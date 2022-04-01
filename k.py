from logging import basicConfig, getLogger, CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
from env3 import Env3
from kindlelist import KindleList
import sys
import argparse
from calibrex import Calibrex
from util import Util
import json

# basicConfig(level=CRITICAL)
# basicConfig(level=ERROR)
# basicConfig(level=WARNING)
# basicConfig(level=INFO)
basicConfig(level=DEBUG)  #デバッグ時にアンコメントしよ
# basicConfig(level=NOTSET)
logger = getLogger(__name__)
logger.debug('main using debug. start running')
logger.debug('main finished running')

def cmd_get(inst, target_name, target):
  response = inst.get_gss('purchase')
  fname = "get.json"
  Util.json2file(response, fname)

def cmd_append(inst, target_name, target):
  nary = []
  inst.db2gss_append('purchase')

def cmd_create(inst, target_name, target):
  logger.info('cmd_create')
  inst.create_table('book')
  inst.create_table('purchase')
  inst.create_table('progress')

def cmd_update(inst, target_name, target):
  #inst = Calibrex(target, CMD)
  nary = []
  ret = inst.src2db('book', nary)
  #inst.db2gss_update('book')
  listx = []
  ret = inst.get_id_from_db('book', listx)
  dictx = { x[1]:x[0] for x in listx }
  nary_purchase = inst.dictarray_for_purchase(nary, dictx)
  #self.dictarray2db('purchase', nary_purchase)
  nary_purchase = [ it for it in nary_purchase if it != None and it.get('purchase_date', None) != None ]
  inst.dictarray2db('purchase', nary_purchase)
  logger.debug('nary_purchase={}'.format(nary_purchase))
  inst.db2gss_update('purchase')

def cmd_update_for_bookstore(inst, target_name, target, year):
  nary = []
  inst.cmd_update(target_name, target, year)
  logger.debug('appbase.py | cmd_update_for_bookstore')
  sheetname = 'sheet1'

def cmd_batchUpdate2(inst, target_name, target):
  logger.debug('appbase.py | cmd_batchUpdate2')
  inst.db2gss_batchUpdate2('purchase')

def get_inst(envx, target_name, cmd, year = None):
  if not target_name in envx.d['klass']:
    logger.critical("{} is not in env.d".format(target_name))
    logger.critical("{}".format(env.d['klass']))
    return [None, None]
  if target_name == 'bookstore':
    specific_env = envx.d[target_name][year]
  else:
    specific_env = envx.d[target_name]

  if specific_env == None:
    logger.critical("{} is None".format(target_name))
    logger.critical("{} is None".format(envx.d[target_name]))
    logger.critical("year={}".format(year))
    return [None, None]

  gcp = envx.d['gcp']
  if cmd == 'create':
    db_fname = specific_env.get_new_db_fname()
    print("get_inst db_fname={}".format(db_fname))
    specific_env.set_db_fname( db_fname )
  elif cmd == 'update':
    db_fname = specific_env.get_latest_db_fname()
    print(db_fname)
    print("1 =====================")
    exit(0)
    specific_env.set_db_fname( db_fname )

  klass = envx.d['klass'][target_name]
  inst = klass(specific_env, gcp, cmd)

  return [specific_env, inst]

def not_white_space(s):
  if s == "":
    return False
  else:
    return True

def len_11(s):
  if len(s) > 11:
    return True
  else:
    return False

def to_integer(val):
  return int(val)

def to_string(val):
  return str(val)


def convert_for_table( key , value ):
  dictx = {'totalID': to_integer, 'xid': to_integer, 'purchase_date': to_string,
  'bookstore': to_string, 'title': to_string, 'ASIN': to_string,
  'read_status': to_integer, 'shape': to_integer, 'category': to_string}
  return dictx[key]( value )

def reform_row(row):
  return list(filter(not_white_space, row))

def cmd_jsonx(year=None):
  if year == None:
    fname = "book.json"
  else:
    fname = "book-{}.json".format(year)

  with open(fname, mode='r', encoding='utf-8') as f:
    content = f.read()
  response = json.loads(content)
  len_11_obj = filter(len_11, response['values'][1:])
  map_obj = map(reform_row, len_11_obj)
  headers = reform_row( response['values'][0] )
  xlistx = [ { z[0]:convert_for_table(z[0], z[1]) for z in zip(headers, row) } for row in map_obj]
  for l in xlistx:
    logger.debug(l)

def db_process(envx, target_name, cmd, year = None):
  logger.info( "%s %s %s" % (target_name, cmd, year))
  if cmd == 'createall':
    if target_name == 'bookstore':
      for y in range(2014, 2023):
        year = "{}".format(y)
        specific_env, inst = get_inst(envx, target_name, cmd, year)
        cmd_create(inst, target_name, specific_env)
    else:
      pass
    return None
  elif cmd == 'updateall':
    if target_name == 'bookstore':
      for y in range(2014, 2023):
        specific_env, inst = get_inst(envx, target_name, cmd, y)
        cmd_update_for_bookstore(inst, target_name, specific_env, y)
    else:
      pass
    return None

  specific_env, inst = get_inst(envx, target_name, cmd, year)
  logger.info( "{} {}".format(specific_env, inst))
  
  if specific_env == None:
    return

  if cmd == 'get':
    cmd_get(inst, target_name, specific_env)
  elif cmd == 'create':
    logger.info( "call cmd_create")
    cmd_create(inst, target_name, specific_env)
  elif cmd == 'update':
    if target_name == 'bookstore':
      cmd_update_for_bookstore(inst, target_name, specific_env, year)
    else:
      cmd_update(inst, target_name, specific_env)
  elif cmd == 'batchupdate':
    logger.debug('k.py | batchupdate')
    cmd_batchUpdate(inst, target_name, specific_env)
  elif cmd == 'batchupdate2':
    logger.debug('k.py | batchupdate2')
    cmd_batchUpdate2(inst, target_name, specific_env)
  elif cmd == 'append':
    cmd_append(inst, target_name, specific_env)
  elif cmd == 'json':
    fname = "get.json"
    with open(fname, mode='r', encoding='utf-8') as f:
      content = f.read()
    response = json.loads(content)
    list1 = response['sheets']
    list2 = [ it['data'] for it in list1]
    list3 = [ x['rowData'] for x in list2[0]]
    x = json.dumps(list3, separators=(',', ':'), sort_keys=True, indent=4)
    logger.debug(x)
  elif cmd == 'json2':
    cmd_jsonx(year)
  elif cmd == 'jsonall':
    for y in range(2014, 2023):
      year = "{}".format(y)
      cmd_jsonx(year)
  else:
    logger.error("unknown command: {}".format(cmd))
    sys.exit(1)
  inst.db_close()

parser = argparse.ArgumentParser(description='Process Google Spreadsheet')
#parser = argparse.ArgumentParser('')
parser.add_argument('target', help='target', choices=['kindle', 'kindlejson', 'kindlelist', 'calibre', 'bookstore'])
parser.add_argument('cmd', help='cmd', choices=['create', 'createall',
                                                'update','updateall', 'json','json2', 'jsonall'])
parser.add_argument('year', metavar='year' , type=int, nargs='?', default=-1, help='year')
args = parser.parse_args(sys.argv[1:])
TARGET = args.target.lower()
CMD = args.cmd.lower()
YEAR = "{}".format(args.year)
if CMD == 'createall' or CMD == 'updateall':
  if TARGET != 'bookstore':
    args2 = parser.parse_args(['-h'])
elif TARGET == 'bookstore':
  if YEAR == -1:
    args2 = parser.parse_args(['-h'])

# basicConfig(level=CRITICAL)
# basicConfig(level=ERROR)
# basicConfig(level=WARNING)
basicConfig(level=INFO)
#basicConfig(level=DEBUG)  #デバッグ時にアンコメントしよ
# basicConfig(level=NOTSET)
env3 = Env3()
db_process(env3, TARGET, CMD, YEAR)
