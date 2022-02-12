from sqlite3db import Sqlite3db
# from ndl import Ndl

class AppDb:
  def __init__(self, db_file, table_name, table_def_stmt):
    self.table_name = table_name
    self.table_def_stmt = table_def_stmt
    ensure_sql = 'SELECT id FROM {0} WHERE id = 1'.format(self.table_name)
    self.db = Sqlite3db(db_file, self.table_def_stmt, ensure_sql)
    print("AppDb.__init__: db_file={0}".format(db_file))
    self.insert_sql = '''INSERT INTO {0}
     (ASIN, title, authors, publishers, publication_date, purchase_date, textbook_type, cde_contenttype, content_type)
     VALUES (:ASIN, :title, :authors, :publishers, :publication_date, :purchase_date, :textbook_type, :cde_contenttype, :content_type)'''.format(self.table_name)

  def ensure_connect(self):
    self.db.ensure_connect()

  def test_insert(self, val):
    try:
      sql = "INSERT INTO test (val) VALUES ('{0}')"
      stmt = sql.format(val)
      print(stmt)
      self.db.execute_and_commit(stmt)
      ret = True
    except self.db.sqlite3.ProgrammingError as err:
      print('1-T sqlite3.ProgrammingError: {0}'.format(err))

    return ret

  def insert_all(self, data_list):
    ret = False
    try:
      for dict_rec in data_list:
        self.db.execute(self.insert_sql, dict_rec)
      ret = True
    except self.db.sqlite3.ProgrammingError as err:
      print('1-1 sqlite3.ProgrammingError: {0}'.format(err))

    if ret == True:
      self.db.commit()

    return ret

  def insert(self, ASIN, title, authors, publishers, publication_date, purchase_date, textbook_type, cde_contenttype, content_type):
    ret = False
    try:
      sql = "INSERT INTO {0} (ASIN, title, authors, publishers, publication_date, purchase_date, textbook_type, cde_contenttype, content_type) VALUES ('{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')"
      #self.db.execute_and_commit(sql.format(self.table_name, ASIN, title, authors, publishers, publication_date, purchase_date, textbook_type, cde_contenttype, content_type))
      stmt = sql.format(self.table_name, ASIN, title, authors, publishers, publication_date, purchase_date, textbook_type, cde_contenttype, content_type)
      #print(stmt)
      self.db.execute_and_commit(stmt)
      ret = True
    except self.db.sqlite3.ProgrammingError as err:
      print('1-2 sqlite3.ProgrammingError: {0}'.format(err))

    return ret

  def update(self, ASIN, stock):
    ret = False
    try:
      self.db.execute_and_commit('UPDATE bookshelf SET stock = "{0}" WHERE ASIN = "{1}"'.format(stock, ASIN))
      ret = True
    except self.db.sqlite3.ProgrammingError as err:
      print('1-3 sqlite3.ProgrammingError: {0}'.format(err))

    return ret

  def select_one(self, value):
    ret = False
    cursor = None

    try:
      cursor = self.db.execute('SELECT * FROM {0} WHERE ASIN = "{1}"'.format(self.table_name, value))
      #print("select_one: A")
      if cursor != None:
        #print("select_one: B")
        lista = cursor.fetchall()

        size = len( lista )
        if size == 1:
          for x in lista:
            for y in x:
              pass
          ret = True
    except self.db.sqlite3.ProgrammingError as err:
      print('1-5 sqlite3.ProgrammingError: {0}'.format(err))

    return ret

  def select_none(self, value):
    ret = False
    cursor = None

    try:
      cursor = self.db.execute('SELECT * FROM {0} WHERE ASIN = "{1}"'.format(self.table_name, value))
      if cursor != None:
        size = len( cursor.fetchall() )
        if size == 0:
          ret = True
    except self.db.sqlite3.ProgrammingError as err:
      print('1-6 sqlite3.ProgrammingError: {0}'.format(err))

    return ret

  def select_all_as_dict(self, list):
    cursor = None
    ret = False

    try:
      cursor = self.db.execute('SELECT * FROM {0}'.format(self.table_name))
      if cursor != None:
        for r in cursor.fetchall():
          list.append( {'id': r['id'], 'ASIN': r['ASIN'], 'title': r['title'], 'authors': r['authors'], 'publishers': r['publishers'], 
                      'publication_date': r['publication_date'], 'purchase_date': r['purchase_date'], 'textbook_type': r['textbook_type'], 
                      'cde_contenttype': r['cde_contenttype'], 'content_type': r['content_type']} )
        ret = True
    except self.db.sqlite3.ProgrammingError as err:
      print('1-4 sqlite3.ProgrammingError: {0}'.format(err))

    return ret

  def select_all(self, list):
    cursor = None
    ret = False

    try:
      cursor = self.db.execute('SELECT * FROM {0}'.format(self.table_name))
      if cursor != None:
        for r in cursor.fetchall():
          list.append( [r['id'], r['ASIN'], r['title'], r['authors'], r['publishers'], 
                        r['publication_date'], r['purchase_date'], r['textbook_type'], 
                        r['cde_contenttype'], r['content_type'] ] )
        ret = True
    except self.db.sqlite3.ProgrammingError as err:
      print('1-4 sqlite3.ProgrammingError: {0}'.format(err))

    return ret

  def close(self):
    self.db.close()

  def get(self):
    ret = False
    rows = []

    try:
      self.cur.execute('SELECT * FROM {0}'.format(self.table_name))
      for r in self.cur.fetchall():
        rows.append( {'id': r['id'], 'ASIN': r['ASIN'], 'title': r['title'], 'authors': r['authors'], 'publishers': r['publishers'],
                      'publication_date': r['publication_date'], 'purchase_date': r['purchase_date'],
                      'textbook_type': r['textbook_type'], 'cde_contenttype': r['cde_contenttype'], 'content_type': r['content_type']} )
      ret = True
    except self.db.sqlite3.ProgrammingError as err:
      print('1-7 sqlite3.ProgrammingError: {0}'.format(err))

    return rows

  def set(self, values):
    ret = False
    place_holder = ','.join('?'*len(values))
    sql = f'INSERT INTO {self.table_name} VALUES ({place_holder})'

    try:
      self.db.execute(sql, values)
      self.conn.commit()
      ret = True
    except self.db.sqlite3.ProgrammingError as err:
      print('1-8 sqlite3.ProgrammingError: {0}'.format(err))

    return ret
