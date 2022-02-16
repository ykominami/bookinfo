from logging import basicConfig, getLogger, DEBUG
from sqlite3 import dbapi2
from sqlite3db import Sqlite3db


# basicConfig(level=DEBUG)  デバッグ時にアンコメントしよ

class AppDb:
  def __init__(self, cmd, db_file, table_name, table_def_stmt):
    self.logger = getLogger(__name__)
    self.logger.debug('using debug. start running')
    self.logger.debug('finished running')

    self.cmd = cmd
    self.db_file = db_file
    self.table_name = table_name
    self.table_def_stmt = table_def_stmt
    self.ensure_sql = 'SELECT id FROM {0} WHERE id = 1'.format(self.table_name)
    self._db = Sqlite3db(self.cmd, self.db_file, self.table_def_stmt, self.ensure_sql)
    self.logger.debug("AppDb.__init__: db_file={0}".format(db_file))
    self.insert_sql = '''INSERT INTO {0}
     (ASIN, title, authors, publishers, publication_date, purchase_date, textbook_type, cde_contenttype, content_type)
     VALUES (:ASIN, :title, :authors, :publishers, :publication_date, :purchase_date, :textbook_type, :cde_contenttype, :content_type)'''.format(self.table_name)
    self.insert_sql_2 = '''INSERT INTO {0} (ASIN) VALUES (:ASIN)'''.format(self.table_name)

  @property
  def db(self):
    return self._db

  @db.setter
  def db(self, arg):
    self._db = arg

  def create_table(self):
    self.logger.debug("AppDb create_table")
    self.db.create_table_and_commit()
    self.db.close()

  def insert_all_and_commit(self, data_list):
    ret = False
    count = 0
    for dict_rec in data_list:
      try:
        cursor, execute_ret = self.db.execute(self.insert_sql, dict_rec)
        count += 1
      except self.db.sqlite3.ProgrammingError as err:
        self.logger.error('appdb.py 1-1 sqlite3.ProgrammingError: {0}'.format(err))
        execute_ret = False
      except self.db.sqlite3.OperationalError as err:
        self.logger.error('appdb.py 1-2 sqlite3.OperationalError: {0}'.format(err))
        self.logger.error('appdb.py self.insert_sql=%s' % self.insert_sql)
        execute_ret = False

  def insert_unique_record_all_and_commit(self, data_list):
    ret = False
    count = 0
    for dict_rec in data_list:
      if self.select_none(dict_rec['ASIN']) == True:
        try:
          cursor, execute_ret = self.db.execute(self.insert_sql, dict_rec)
          count += 1
        except self.db.sqlite3.ProgrammingError as err:
          self.logger.error('appdb.py 1-1 sqlite3.ProgrammingError: {0}'.format(err))
          execute_ret = False
        except self.db.sqlite3.OperationalError as err:
          self.logger.error('appdb.py 1-2 sqlite3.OperationalError: {0}'.format(err))
          self.logger.error('appdb.py self.insert_sql=%s' % self.insert_sql)
        execute_ret = False

    if count > 0:
      self.db.commit()
      self.logger.debug("self.db_commit")
      ret = True

    return ret

  def insert_and_commit(self, ASIN, title, authors, publishers, publication_date, purchase_date, textbook_type, cde_contenttype, content_type):
    ret = False
    try:
      sql = "INSERT INTO {0} (ASIN, title, authors, publishers, publication_date, purchase_date, textbook_type, cde_contenttype, content_type) VALUES ('{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')"
      #self.db.execute_and_commit(sql.format(self.table_name, ASIN, title, authors, publishers, publication_date, purchase_date, textbook_type, cde_contenttype, content_type))
      stmt = sql.format(self.table_name, ASIN, title, authors, publishers, publication_date, purchase_date, textbook_type, cde_contenttype, content_type)
      #self.logger.debug(stmt)
      cursor, execute_ret = self.db.execute_and_commit(stmt)
      ret = execute_ret
    except self.db.sqlite3.ProgrammingError as err:
      self.logger.error('1-2 sqlite3.ProgrammingError: {0}'.format(err))

    return ret

  def update(self, ASIN, stock):
    ret = False
    try:
      cursor, execute_ret = self.db.execute_and_commit('UPDATE bookshelf SET stock = "{0}" WHERE ASIN = "{1}"'.format(stock, ASIN))
      ret = execute_ret
    except self.db.sqlite3.ProgrammingError as err:
      self.logger.error('1-3 sqlite3.ProgrammingError: {0}'.format(err))

    return ret

  def select_one_record(self, value, specified_num):
    ret = False
    cursor = None
    records = []

    try:
      sql = 'SELECT * FROM {0} WHERE ASIN = "{1}"'.format(self.table_name, value)
      cursor, execute_ret = self.db.execute(sql)
      #self.logger.debug("select_one: A")
      if (execute_ret == True) & (cursor != None):
        #self.logger.debug("select_one: B")
        records = cursor.fetchall()
        size = len( records )
        if size == specified_num:
          ret = True
    except self.db.sqlite3.ProgrammingError as err:
      self.logger.error('1-5 sqlite3.ProgrammingError: {0}'.format(err))

    return [ret, records]

  def select_one(self, value):
    ret, records = self.select_one_record(value, 1)
    return ret

  def select_none(self, value):
    ret, records = self.select_one_record(value, 0)
    return ret

  def select_all_as_dict(self, list):
    cursor = None
    ret = False

    try:
      cursor, execute_ret = self.db.execute('SELECT * FROM {0}'.format(self.table_name))
      if (execute_ret == True) & (cursor != None):
        for r in cursor.fetchall():
          list.append( {'id': r['id'], 'ASIN': r['ASIN'], 'title': r['title'], 'authors': r['authors'], 'publishers': r['publishers'], 
                      'publication_date': r['publication_date'], 'purchase_date': r['purchase_date'], 'textbook_type': r['textbook_type'], 
                      'cde_contenttype': r['cde_contenttype'], 'content_type': r['content_type']} )
        ret = True
    except self.db.sqlite3.ProgrammingError as err:
      self.logger.error('1-4 sqlite3.ProgrammingError: {0}'.format(err))

    return ret

  def select_all(self, list):
    cursor = None
    ret = False

    try:
      cursor, execute_ret = self.db.execute('SELECT * FROM {0}'.format(self.table_name))
      if (execute_ret == True) & (cursor != None):
        for r in cursor.fetchall():
          list.append( [r['id'], r['ASIN'], r['title'], r['authors'], r['publishers'], 
                        r['publication_date'], r['purchase_date'], r['textbook_type'], 
                        r['cde_contenttype'], r['content_type'] ] )
        ret = True
    except self.db.sqlite3.ProgrammingError as err:
      self.logger.error('1-4 sqlite3.ProgrammingError: {0}'.format(err))

    return ret

  def close(self):
    self.db.close()
