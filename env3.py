from logging import basicConfig, getLogger, DEBUG
import os
#import os.path
from pathlib import Path
#import pyocr
#import pyocr.builders
from kindlelist import KindleList
from calibrex import Calibrex
class Env3:
  class EnvTarget:
    @property
    def d(self):
      return self.__d

    @d.setter
    def d(self, value):
      self.__d = value

    def __init__(self, dict):
      self.logger = getLogger(__name__)
      self.logger.debug('using debug. start running')
      self.logger.debug('finished running')

      self.d = dict

    def get_db_fname(self, db_fname_base, num, ext):
      fn = "%s%d.%s" % (db_fname_base, num, ext)
      return fn

    def _get_latest_db_fname(self, db_fname_base, num, ext):
      fn = ""
      latest_fn = ""
      while True:
        latest_fn = fn
        fn = "%s%d.%s" % (db_fname_base, num, ext)
        if not os.path.exists(fn):
          break
        num += 1

      return latest_fn

    def get_latest_db_fname(self):
      db = self.d['db']
      fname_base = db['db_fname_base']
      self.logger.debug("fname_base=%s" % (fname_base))
      num = db['db_id']
      ext = db['db_file_ext']
      return self._get_latest_db_fname(fname_base, num, ext)

    def _get_new_db_fname(self, db_fname_base, num, ext):
      while True:
        fn = "%s%d.%s" % (db_fname_base, num, ext)
        if not os.path.exists(fn):
          break
        num += 1

      return fn

    def get_new_db_fname(self):
      db = self.d['db']
      fname_base = db['db_fname_base']
      self.logger.debug("fname_base=%s" % (fname_base))
      num = db['db_id']
      ext = db['db_file_ext']
      return self._get_new_db_fname(fname_base, num, ext)

    def set_db_fname(self, db_fname):
      db = self.d['db']
      db['db_file'] = db_fname

  @property
  def calibre(self):
    return self.__calibre
  @calibre.setter
  def calibre(self, value):
    self.__calibre = value

  def init_kindle(self):
    kind = 'kindle'
    fname_base_kindle = 'kindle'
    db_fname_base_kindle = self.db_dir / fname_base_kindle
    xml_headers_kindle = ['ASIN', 'title', 'authors', 'publishers', 'publication_date', 
                'purchase_date', 'textbook_type', 'cde_contenttype', 'content_type']
    table_columns_default_kindle = ['id']
    table_columns_kindle_book = table_columns_default_kindle + xml_headers_kindle
    text_fields_kindle_book = ['title', 'authors', 'publishers']
    text_fields_kindle_purchase = []
    text_fields_kindle_progress = []

    #  'kindle_cache_file':r'C:\Users\ykomi\AppData\Local\Amazon\Kindle\Cache\KindleSyncMetadataCache.xml',
    dict_kindle_db = {
      'db_id':0,
      'db_fname_base':db_fname_base_kindle,
      'db_file_ext':r'sqlite',
      'encoding':'utf_8_sig',
      'newline':"",
      'kindle_cache_file':r'Z:\BACKUP\ykomi-202008\AppData\Local\Amazon\Kindle\Cache\KindleSyncMetadataCache.xml',
    }
    # kindle-list-2022
    # 1bx2wC_XhNvQOhdNiK1JTx1UcfXHMHpsMelxuhk0yrEo
    dict_kindle_book = {
      'table_name':'book',
      'xml_headers':xml_headers_kindle ,
      'table_columns':table_columns_kindle_book,
      'text_fields':text_fields_kindle_book,
      'id_field':'ASIN',
      'SPREADSHEET_ID':'1h7HE9S3fzDVa8TclQySC_bokN8v6bGmYL-VrKjm6iXM',
      'SAMPLE_RANGE_NAME':'A2:E',
      'RANGE_NAME':'sheet10!A1:Z',
      'MAJOR_DIMENSION':'ROWS',
      'clear_range':'A1:J',
      'id_related_columns':['id', 'ASIN'],
    }
    # kindle-list-2022-purchase
    # 1NwPrKR44R_4DEH4U-QsB78EspCBuA-pMPX5TDxmU7eM
    dict_kindle_purchase = {
      'table_name':'purchase',
      'text_fields':text_fields_kindle_purchase,
      'id_field':'ext_id',
      'SPREADSHEET_ID':'1NwPrKR44R_4DEH4U-QsB78EspCBuA-pMPX5TDxmU7eM',
      'SAMPLE_RANGE_NAME':'A2:E',
      'RANGE_NAME':'A1',
      'MAJOR_DIMENSION':'ROWS',
      'clear_range':'A1:J',
    }
    # kindle-list-2022-progress
    # 1lyhqepzQXFsqe54tMdn_QNDPi6JlVip_e7c-gx5SQN0
    dict_kindle_progress = {
      'table_name':'progress',
      'text_fields':text_fields_kindle_progress,
      'SPREADSHEET_ID':'1lyhqepzQXFsqe54tMdn_QNDPi6JlVip_e7c-gx5SQN0',
      
    }

    dict_kindle = {
      'db':dict_kindle_db,
      'book':dict_kindle_book,
      'purchase':dict_kindle_purchase,
      'progress':dict_kindle_progress,
    }

    obj = self.EnvTarget(dict_kindle)

    db = obj.d['db']
    db['db_file'] = obj.get_db_fname(
      db['db_fname_base'], 
      db['db_id'], 
      db['db_file_ext'])
    book = obj.d['book']
    book['table_def_stmt'] = f"""CREATE TABLE if not exists {book['table_name']} (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ASIN STRING UNIQUE,
      title STRING,
      authors STRING,
      publishers STRING,
      publication_date TEXT,
      purchase_date TEXT,
      textbook_type STRING,
      cde_contenttype STRING,
      content_type STRING
)"""

    purchase = obj.d['purchase']
    purchase['table_def_stmt'] = f"""CREATE TABLE if not exists {purchase['table_name']} (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ASIN STRING UNIQUE,
      ext_id INTEGER UNIQUE,
      purchase_date TEXT,
      year STRING,
      month STRING,
      day STRING,
      year_month STRING,
      year_month_day STRING,
      foreign key (ext_id) references book(id) 
      )"""

    progress = obj.d['progress']
    progress['table_def_stmt'] = f"""CREATE TABLE if not exists {progress['table_name']} (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ASIN STRING UNIQUE,
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
     (ASIN, title, authors, publishers, publication_date, purchase_date, textbook_type, cde_contenttype, content_type)
     VALUES (:ASIN, :title, :authors, :publishers, :publication_date, :purchase_date, :textbook_type, :cde_contenttype, :content_type)'''.format(book['table_name'])

    purchase['insert_sql'] = '''INSERT INTO {0}
            ( ASIN,  ext_id,  purchase_date, year, month, day, year_month, year_month_day)
     VALUES (:ASIN, :ext_id, :purchase_date, :year, :month, :day, :year_month, :year_month_day)'''.format(obj.d['purchase']['table_name'])

    progress['insert_sql'] = '''INSERT INTO {0}
            ( ASIN,  ext_id,  status,  progress_date,  year,  month,  day,  year_month,  year_month_day)
     VALUES (:ASIN, :ext_id, :status, :progress_date, :year, :month, :day, :year_month, :year_month_day)'''.format(obj.d['progress']['table_name'])

    return obj

  def init_calibre(self):
    kind = 'calibre'
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

    obj = self.EnvTarget(dict_calibre)

    db = obj.d['db']
    db['db_file'] = obj.get_db_fname(
      db['db_fname_base'], 
      db['db_id'], 
      db['db_file_ext'])

    book = obj.d['book']
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

    purchase = obj.d['purchase']
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

    progress = obj.d['progress']
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
     VALUES (:xxid, :ext_id, :purchase_date, :year, :month, :day, :year_month, :year_month_day)'''.format(obj.d['purchase']['table_name'])

    progress['insert_sql'] = '''INSERT INTO {0}
            ( xxid,  ext_id,  status,  progress_date,  year,  month,  day,  year_month,  year_month_day)
     VALUES (:xxid, :ext_id, :status, :progress_date, :year, :month, :day, :year_month, :year_month_day)'''.format(obj.d['progress']['table_name'])

    return obj

  def __init__(self):
    # ykominami@gmail.com
    self.logger = getLogger(__name__)
    self.logger.debug('using debug. start running')
    self.logger.debug('finished running')

    self.d = {}
    self.d['klass'] = { 'kindle':KindleList, 'calibre':Calibrex}
    #self.d['calibre'] = init_calibre()
    self.d['gcp'] = {}
    self.d['gcp']['credentials'] = 'client_secret_855711122174-5itvr3iu0fpa5un9fvl6j3f1qu1su19m.apps.googleusercontent.com.json'
    #self.d['gcp']['token'] = 'token.json'
    self.d['gcp']['token'] = 'token.pickle'
    self.d['gcp']['SCOPES'] = ['https://www.googleapis.com/auth/spreadsheets']
    self.db_dir = Path( r'C:\Users\ykomi\cur\python\kindledb' )

    self.d['kindle'] = self.init_kindle()
    self.d['calibre'] = self.init_calibre()


if __name__ == '__main__':
  env3 = Env3()
  self.logger.debug( env3.db_id )
