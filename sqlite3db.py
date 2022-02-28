from logging import basicConfig, getLogger, DEBUG
import sqlite3
from pathlib import Path
import os

class Sqlite3db:
  def init_for_create(self, path):
    if not path.exists():
      self.valid_db = True

  def init_for_update(self, path):
    self.logger.debug("init_for_update   -----------")
    self.logger.debug(path)
    if path.exists():
      statinfo = os.stat(path)
      if statinfo.st_size > 0:
        self.valid_db = True
    self.logger.debug("init_for_update E -----------")

  #def __init__(self, cmd, db_file, table_def_stmt):
  def __init__(self, cmd, db_file, env):
    self.logger = getLogger(__name__)
    self.logger.debug('using debug. start running')
    self.logger.debug('finished running')

    self.sqlite3 = sqlite3
    self.db_file = db_file
    self.env = env
    #self.table_def_stmt = table_def_stmt

    #self.table_def = False
    self.conn = None
    self.cursor = None
    self.valid_db = False
    path = Path(db_file)
    if cmd == 'CREATE':
      self.init_for_create(path)
    else:
      self.init_for_update(path)
      #
    self.connect()

  def dict_factory(self, cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
      d[col[0]] = row[idx]
    return d

  def connect(self):
    self.logger.debug("sqlite3db.py connect=")
    self.logger.debug(self.conn)
    self.logger.debug("self.db_file=%s" % (self.db_file))

    if self.conn == None:
      self.logger.debug(self.db_file)
      self.conn = sqlite3.connect(self.db_file, check_same_thread = False,
        detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
      sqlite3.dbapi2.converters['DATETIME'] = sqlite3.dbapi2.converters['TIMESTAMP']
      #self.conn.row_factory = sqlite3.Row
      self.conn.row_factory = self.dict_factory
      self.logger.debug("sqlite3db.py connect None -> conn={}".format(self.conn))

    self.logger.debug("sqlite3db.py 2 connect=")
    self.logger.debug(self.conn)
    self.cursor = self.conn.cursor()
    self.logger.debug(self.cursor)

  def create_table_and_commit(self, key):
    self.create_table(key)
    # データベースへコミット。これで変更が反映される。
    self.conn.commit()

  def create_table(self, key):
    ret = False
    cursor = self.get_cursor()
    #cursor)
    try:
      sql = self.env.d[key]['table_def_stmt']
      cursor.execute(sql)
      ret = True
    except sqlite3.OperationalError as err:
      self.logger.error( "Sqlite3db create_table sqlite3.OperationalError: {0}".format(err) )

    return [cursor, ret]

  def get_cursor(self):
    if self.cursor == None:
      self.cursor = self.conn.cursor()

    return self.cursor

  def execute(self, statement, varlist = None):
    ret = False
    cursor = self.get_cursor()

    try:
      if varlist == None:
        cursor.execute(statement)
        ret = True
      else:
        cursor.execute(statement, varlist)
        ret = True
    except sqlite3.IntegrityError as err:
      self.logger.error( "Sqlite3db execute sqlite3.IntegrityError: {0}".format(err) )

    return [cursor, ret]

  def execute_and_commit(self, statement):
    ret = False
    cursor = self.get_cursor()
    try:
      cursor.execute(statement)
      self.conn.commit()
      ret = True
    except sqlite3.IntegrityError as err:
      self.logger.error( "Sqlite3db execute sqlite3.IntegrityError: {0}".format(err) )

    return [cursor, ret]

  def commit(self):
    self.conn.commit()

  def close_cursor(self):
    if self.cursor != None:
      try:
        self.cursor.close()
      except sqlite3.ProgrammingError as err:
        self.logger.error( "Sqlite3db close_cursor sqlite3.ProgrammingError: {0}".format(err) )

      self.cursor = None

  def close_conn(self):
    if self.conn != None:
      self.conn.close()
      self.conn = None

  def close(self):
    self.close_cursor()
    self.close_conn()
