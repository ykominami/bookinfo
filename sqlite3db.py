import sqlite3
from pathlib import Path
import os

class Sqlite3db:
  def __init__(self, db_file, table_def_stmt, ensure_sql):
    self.sqlite3 = sqlite3
    self.db_file = db_file
    self.table_def_stmt = table_def_stmt
    self.ensure_sql = ensure_sql

    self.table_def = False
    self.conn = None
    self.cursor = None
    self.valid_db = False
    p = Path(db_file)
    if p.exists():
      statinfo = os.stat(p)
      if statinfo.st_size > 0:
        self.valid_db = True

    self.connect()
    if self.valid_db == False:
      print("Sqlite3db __init__ 1")
      self.create_table()
      # データベースへのコネクションを閉じる。(必須)
      #self.close_conn()
      print("Sqlite3db __init__ 1_END")
    else:
      print("Sqlite3db __init__ 2")

  def connect(self):
    if self.conn == None:
      self.conn = sqlite3.connect(self.db_file, check_same_thread = False,
        detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
      sqlite3.dbapi2.converters['DATETIME'] = sqlite3.dbapi2.converters['TIMESTAMP']
      self.conn.row_factory = sqlite3.Row

  def ensure_connect(self):
    retry_count = 0

    self.connect()

    while retry_count < 3:
      try:
#        cursor = self.sqlite3.execute(self.ensure_sql)
        cursor = self.conn.execute(self.ensure_sql)
      except sqlite3.ProgrammingError as err:
        print('5 sqlite3.ProgrammingError: {0}'.format(err))
        state = False

      if cursor == None:
        self.connect()
      else:
        break

      retry_count += 1

  def create_table(self):
    cursor = self.get_cursor()
    #cursor)
    try:
      cursor.execute(self.table_def_stmt)
      # データベースへコミット。これで変更が反映される。
      self.conn.commit()
      self.close_conn()
    except sqlite3.OperationalError as err:
      print( "Sqlite3db create_table sqlite3.OperationalError: {0}".format(err) )


  def get_cursor(self):
    if self.cursor == None:
      self.cursor = self.conn.cursor()

    return self.cursor

  def execute(self, statement, varlist = None):
    cursor = self.get_cursor()
    try:
      if varlist == None:
        cursor.execute(statement)
      else:
        #print(statement)
        #print(varlist)
        cursor.execute(statement, varlist)
    except sqlite3.IntegrityError as err:
      print( "Sqlite3db execute sqlite3.IntegrityError: {0}".format(err) )

    return cursor

  def execute_and_commit(self, statement):
    # self.connect()
    cursor = self.get_cursor()
    try:
      cursor.execute(statement)
      self.conn.commit()
    except sqlite3.IntegrityError as err:
      print( "Sqlite3db execute sqlite3.IntegrityError: {0}".format(err) )

    return cursor

  def commit(self):
    self.conn.commit()

  def close_cursor(self):
    if self.cursor != None:
      try:
        self.cursor.close()
      except sqlite3.ProgrammingError as err:
        print( "Sqlite3db close_cursor sqlite3.ProgrammingError: {0}".format(err) )

      self.cursor = None

  def close_conn(self):
    if self.conn != None:
      self.conn.close()
      self.conn = None

  def close(self):
    self.close_cursor()
    self.close_conn()


