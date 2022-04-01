from envtarget import EnvTarget

class EnvCalibre:
  def __init__(self, db_dir):
    kind = 'calibre'
    self.db_dir = db_dir
    fname_base_calibre = 'calibre'
    db_fname_base_calibre = self.db_dir / fname_base_calibre

    table_columns_calibre_default = ['xid', 'xxid']
    incsv_headers_calibre_book = ['isbn','id','uuid','comments','size','series','series_index','title','title_sort','tags','library_name','formats','timestamp','pubdate','publisher','authors','author_sort','cover','languages','rating','identifiers']
    table_columns_calibre_book = table_columns_calibre_default + incsv_headers_calibre_book
    text_fields_calibre_book = ['comments','series','title','title_sort','tags','library_name','formats','publisher','authors','author_sort']
    text_fields_calibre_purchase = []
    text_fields_calibre_progress = []

    dict_calibre_db = {
      'db_id':0,
      'db_fname_base':db_fname_base_calibre,
      'db_file_ext':r'sqlite',
      'encoding':'utf_8_sig',
      'newline':"",
      'incsvfile':r'C:\Users\ykomi\cur\calibre\マイブック.csv',
    }
    # calibre_list-book
    # 1Mrh9J_b4773WvauJKIf3rWIKfIeZKUMVrZb1hrMLTZo
    dict_calibre_book = {
      'table_name':'book',
      'incsv_headers':incsv_headers_calibre_book ,
      'table_columns':table_columns_calibre_book ,
      'text_fields':text_fields_calibre_book,
      'id_field':'xxid',
      'SPREADSHEET_ID':'1Mrh9J_b4773WvauJKIf3rWIKfIeZKUMVrZb1hrMLTZo',
      'SAMPLE_RANGE_NAME':'A2:E',
      'RANGE_NAME':'A1',
      'MAJOR_DIMENSION':'ROWS',
      'clear_range':'A1:J',
      'id_related_columns':['xid', 'xxid'],
    }
    # calibre-list-purchase
    # 1HvduI_FmuJjJsUzjvhlYuitBXxzOlCEGMtHEWzgCiWk
    dict_calibre_purchase = {
      'table_name':'purchase',
      'text_fields':text_fields_calibre_purchase,
      'id_field':'xxid',
      'SPREADSHEET_ID':'1HvduI_FmuJjJsUzjvhlYuitBXxzOlCEGMtHEWzgCiWk',
      'SAMPLE_RANGE_NAME':'A2:E',
      'RANGE_NAME':'A1',
      'MAJOR_DIMENSION':'ROWS',
      'clear_range':'A1:J',
      'id_related_columns':['xid', 'xxid'],
    }
    # calibre-list-progress
    # 1o0mLOb3cDs7X1FF9L_bJdKBDKW__7M3DGQOFKDuDw94
    dict_calibre_progress = {
      'table_name':'progress',
      'text_fields':text_fields_calibre_progress,
      'id_field':'xxid',
      'SPREADSHEET_ID':'1o0mLOb3cDs7X1FF9L_bJdKBDKW__7M3DGQOFKDuDw94',
    }

    dict_calibre = {
      'db':dict_calibre_db,
      'book':dict_calibre_book,
      'purchase':dict_calibre_purchase,
      'progress':dict_calibre_progress,
    }

    self.target = EnvTarget(dict_calibre)

    db = self.target.d['db']
    db['db_file'] = self.target.get_db_fname(
      db['db_fname_base'],
      db['db_id'],
      db['db_file_ext'])

    book = self.target.d['book']
    book['table_def_stmt'] = f"""CREATE TABLE if not exists {book['table_name']} (
      xid INTEGER PRIMARY KEY AUTOINCREMENT,

      xxid STRING UNIQUE,
      isbn STRING ,
      id NUMBER UNIQUE,
      uuid STRING UNIQUE,
      comments STRING,

      size NUMBER,
      series STRING,
      series_index NUMBER,
      title STRING,
      title_sort STRING,

      tags STRING,
      library_name STRING,
      formats STRING,
      timestamp NUMBER,
      pubdate NUMBER,

      publisher STRING,
      authors STRING,
      author_sort STRING,
      cover STRING,
      languages STRING,

      rating NUMBER,
      identifiers STRING
)"""

    purchase = self.target.d['purchase']
    purchase['table_def_stmt'] = f"""CREATE TABLE if not exists {purchase['table_name']} (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      xxid STRING UNIQUE,
      ext_id INTEGER UNIQUE,
      purchase_date TEXT,
      year STRING,
      month STRING,
      day STRING,
      year_month STRING,
      year_month_day STRING,
      foreign key (ext_id) references book(id)
      )"""

    progress = self.target.d['progress']
    progress['table_def_stmt'] = f"""CREATE TABLE if not exists {progress['table_name']} (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      xxid STRING UNIQUE,
      ext_id INTEGER UNIQUE,
      status INTEGER,
      progress_date TEXT,
      year STRING,
      month STRING,
      day STRING,
      year_month STRING,
      year_month_day STRING,
      foreign key (ext_id) references book(id)
      )"""

    book['insert_sql'] = '''INSERT INTO {0}
      (
      xxid,
      isbn,
      id,
      uuid,
      comments,

      size,
      series,
      series_index,
      title,
      title_sort,

      tags,
      library_name,
      formats,
      timestamp,
      pubdate,

      publisher,
      authors,
      author_sort,
      cover,
      languages,

      rating,
      identifiers
      )

      VALUES(
      :xxid,
      :isbn,
      :id,
      :uuid,
      :comments,

      :size,
      :series,
      :series_index,
      :title,
      :title_sort,

      :tags,
      :library_name,
      :formats,
      :timestamp,
      :pubdate,

      :publisher,
      :authors,
      :author_sort,
      :cover,
      :languages,

      :rating,
      :identifiers
      )'''.format(book['table_name'])

    purchase['insert_sql'] = '''INSERT INTO {0}
            ( xxid,  ext_id,  purchase_date, year, month, day, year_month, year_month_day)
     VALUES (:xxid, :ext_id, :purchase_date, :year, :month, :day, :year_month, :year_month_day)'''.format(self.target.d['purchase']['table_name'])

    progress['insert_sql'] = '''INSERT INTO {0}
            ( xxid,  ext_id,  status,  progress_date,  year,  month,  day,  year_month,  year_month_day)
     VALUES (:xxid, :ext_id, :status, :progress_date, :year, :month, :day, :year_month, :year_month_day)'''.format(self.target.d['progress']['table_name'])

  def get_new_db_fname(self):
    return self.target.get_new_db_fname()

  def set_db_fname(self, db_fname):
    return self.target.set_db_fname(db_fname)