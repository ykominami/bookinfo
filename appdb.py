from logging import basicConfig, getLogger, DEBUG
from sqlite3 import dbapi2
from sqlite3db import Sqlite3db


# basicConfig(level=DEBUG)  デバッグ時にアンコメントしよ

class AppDb:
  #def __init__(self, cmd, db_file, table_name, table_def_stmt, id_field, insert_sql, table_columns):
  def __init__(self, cmd, db_file, specific_env):
    self.logger = getLogger(__name__)
    self.logger.debug('using debug. start running')
    self.logger.debug('finished running')

    self.cmd = cmd
    self.db_file = db_file
    self.specific_env = specific_env
    self._db = Sqlite3db(self.cmd, self.db_file, self.specific_env)

    self.logger.debug("AppDb.__init__: db_file={0}".format(db_file))

  @property
  def db(self):
    return self._db

  @db.setter
  def db(self, arg):
    self._db = arg

  def create_table_and_commit(self, key):
    self.logger.debug("AppDb create_table")
    self.db.create_table_and_commit(key)

  def insert_all_and_commit(self, key, data_list):
    ret = False
    count = 0
    for dict_rec in data_list:
      try:
        cursor, execute_ret = self.db.execute(self.specific_env.obj[key]['insert_sql'], dict_rec)
        count += 1
      except self.db.sqlite3.ProgrammingError as err:
        self.logger.error('appdb.py 1-1 sqlite3.ProgrammingError: {0}'.format(err))
        execute_ret = False
      except self.db.sqlite3.OperationalError as err:
        self.logger.error('appdb.py 1-2 sqlite3.OperationalError: {0}'.format(err))
        self.logger.error('appdb.py self.insert_sql=%s' % self.specific_env.obj[key]['insert_sql'])
        execute_ret = False

  def insert_unique_record_all_and_commit(self, key, data_list):
    ret = False
    count = 0
    for dict_rec in data_list:
      ret = self.select_none(key, dict_rec[self.specific_env.obj[key]['id_field']])
      if ret == True:
        try:
          sql = self.specific_env.obj[key]['insert_sql']
          cursor, execute_ret = self.db.execute(sql, dict_rec)
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

  def select_one_record(self, key, value, specified_num):
    ret = False
    cursor = None
    records = []
    table = self.specific_env.obj[key]
    try:
      sql = 'SELECT * FROM {0} WHERE {1} = "{2}"'.format(table['table_name'], table['id_field'], value)
      cursor, execute_ret = self.db.execute(sql)
      #self.logger.debug("select_one: A")
      if (execute_ret == True) & (cursor != None):
        #self.logger.debug("select_one: B")
        records = cursor.fetchall()
        size = len( records )
        if size == specified_num:
          ret = True
          #self.logger.debug("select_one: C")
    except self.db.sqlite3.ProgrammingError as err:
      self.logger.error('1-5 sqlite3.ProgrammingError: {0}'.format(err))

    return [ret, records]

  def select_one(self, key, value):
    ret, records = self.select_one_record(key, value, 1)
    return ret

  def select_none(self, key, value):
    ret, records = self.select_one_record(key, value, 0)
    return ret

  def select_all_as_dict(self, key, list):
    cursor = None
    ret = False
    table = self.specific_env.obj[key]

    try:
      cursor, execute_ret = self.db.execute('SELECT * FROM {0}'.format(table['table_name']))
      if (execute_ret == True) & (cursor != None):
        columns = None
        for r in cursor.fetchall():
          '''
          list.append( {'id': r['id'], self.id_field: r[id_field], 'title': r['title'], 'authors': r['authors'], 'publishers': r['publishers'], 
                      'publication_date': r['publication_date'], 'purchase_date': r['purchase_date'], 'textbook_type': r['textbook_type'], 
                      'cde_contenttype': r['cde_contenttype'], 'content_type': r['content_type']} )
          '''
          #list.append( { x:r[x] for x in table['table_columns'] } )
          if columns == None:
            columns = r.keys()
          list.append( { x:r[x] for x in columns } )
        ret = True
    except self.db.sqlite3.ProgrammingError as err:
      self.logger.error('1-4 sqlite3.ProgrammingError: {0}'.format(err))

    return ret

  def select_all(self, key, list, columns = None):
    cursor = None
    ret = False
    table = self.specific_env.obj[key]

    try:
      if columns == None:
        sql = 'SELECT * FROM {0}'.format(table['table_name'])
      else:
        columns_str = ','.join(columns)
        sql = 'SELECT {1} FROM {0}'.format(table['table_name'], columns_str)

      self.logger.debug("sql=%s" % sql)
      cursor, execute_ret = self.db.execute(sql)
      self.logger.debug("execute_ret={}".format(execute_ret))
      self.logger.debug("cursor={}".format(cursor))
      if (execute_ret == True) & (cursor != None):
        self.logger.debug("appdb select_all")
        for r in cursor.fetchall():
          if columns == None:
            list.append( [ r.values() ] )
          else:
            list.append( [ r[x] for x in columns ] )
        ret = True
    except self.db.sqlite3.ProgrammingError as err:
      self.logger.error('1-4 sqlite3.ProgrammingError: {0}'.format(err))

    return ret

  def close(self):
    self.db.close()

  def convert_boolean_to_integer(self, nary, boolean_fields=[]):
    self.db.convert_boolean_to_integer(nary, boolean_fields)

  def convert_integer_to_boolean(self, nary, boolean_fields=[]):
    self.db.convert_integer_to_boolean(nary, boolean_fields)
