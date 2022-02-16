from logging import basicConfig, getLogger, DEBUG
import sqlite3
from pathlib import Path
import os

class Sqlite3db:
  def init_for_create(self, p):
    if not p.exists():
      self.valid_db = True

  def init_for_update(self, p):
    self.logger.debug("init_for_update   -----------")
    self.logger.debug(p)
    if p.exists():
      statinfo = os.stat(p)
      if statinfo.st_size > 0:
        self.valid_db = True
    self.logger.debug("init_for_update E -----------")

  def __init__(self, cmd, db_file, table_def_stmt, ensure_sql):
    self.logger = getLogger(__name__)
    self.logger.debug('using debug. start running')
    self.logger.debug('finished running')

    self.sqlite3 = sqlite3
    self.db_file = db_file
    self.table_def_stmt = table_def_stmt
    self.ensure_sql = ensure_sql

    self.table_def = False
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

  def connect(self):
    self.logger.debug("sqlite3db.py connect=")
    self.logger.debug(self.conn)
    self.logger.debug("self.db_file=%s" % (self.db_file))

    if self.conn == None:
      self.conn = sqlite3.connect(self.db_file, check_same_thread = False,
        detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
      sqlite3.dbapi2.converters['DATETIME'] = sqlite3.dbapi2.converters['TIMESTAMP']
      self.conn.row_factory = sqlite3.Row
      self.logger.debug("sqlite3db.py connect None -> conn=", self.conn)

    self.logger.debug("sqlite3db.py 2 connect=")
    self.logger.debug(self.conn)
    self.cursor = self.conn.cursor()
    self.logger.debug(self.cursor)

  def create_table_and_commit(self):
    self.create_table()
    # データベースへコミット。これで変更が反映される。
    self.conn.commit()

  def create_table(self):
    ret = False
    cursor = self.get_cursor()
    #cursor)
    try:
      cursor.execute(self.table_def_stmt)
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
