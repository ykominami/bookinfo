from logging import basicConfig, getLogger, CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
from env3 import Env3
from kindlelist import KindleList
import sys
import argparse

# basicConfig(level=CRITICAL)
# basicConfig(level=ERROR)
# basicConfig(level=WARNING)
basicConfig(level=INFO)
# basicConfig(level=DEBUG)  #デバッグ時にアンコメントしよ
# basicConfig(level=NOTSET)
logger = getLogger(__name__)
logger.debug('using debug. start running')
logger.debug('finished running')

parser = argparse.ArgumentParser()
parser.add_argument('cmd', help='cmd help')
args = parser.parse_args(sys.argv[1:])
#logger.debug("--")
CMD = args.cmd.upper()
#exit()

env3 = Env3()
if CMD == 'CREATE':
  db_fname = env3.get_new_db_fname()
  logger.debug(db_fname)
  logger.debug("------ START")
  env3.set_db_fname( db_fname )
  kindlelist = KindleList(env3, CMD)
  kindlelist.create_table()
  logger.debug("------ END")
else:
  db_fname = env3.get_latest_db_fname()
  logger.debug(db_fname)
  logger.debug("------")
  env3.set_db_fname( db_fname )
  kindlelist = KindleList(env3, CMD)
  #kindlelist.test_csv2db()
  #kindlelist.csv2db_bulk_with_dict()
  #kindlelist.csv2db_with_dict()
  kindlelist.xml2db_with_dict()
  #kindlelist.db2gss()

kindlelist.db_close()
