import os
import os.path
#import pyocr
#import pyocr.builders

class Env2:
  __db_id = 7

  @classmethod
  def get_db_fname(cls, db_fname_base, num, ext):
    print(db_fname_base)
    print(num)
    fn = "%s" % (db_fname_base)
    fn = "%d" % (num)
    fn = "%s%d.%s" % (db_fname_base, num, ext)
    return fn


  @classmethod
  def get_new_db_fname(cls):
    print( type(cls) )
    print( cls )
    cls.db_fname_base.__get__(cls, type(cls))
    type(cls).db_fname_base.__get__(cls, type(cls))
    fname_base = cls.db_fname_base
    print("fname_base=%s" % (fname_base))
    num = cls.db_id
    ext = cls.db_file_ext
    return cls._get_new_db_fname(fname_base, num, ext)

  @classmethod
  def _get_new_db_fname(cls, db_fname_base, num, ext):
    while True:
#      fn = "{}{}.{}".format(db_fname_base, num, ext)
      fn = "%s%d.%s" % (db_fname_base, num, ext)
      if not os.path.exists(fn):
        break
      num += 1

    return fn

  @classmethod
  def set_db_fname(cls, db_fname):
    cls.db_file = db_fname

  @classmethod
  def init(cls):
    # ykominami@gmail.com
    cls.__credentials = 'client_secret_855711122174-5itvr3iu0fpa5un9fvl6j3f1qu1su19m.apps.googleusercontent.com.json'
#    cls.credentials = cls.__credentials
  # kindle-list-2022 - Google Sheets
    cls.__SPREADSHEET_ID = '1bx2wC_XhNvQOhdNiK1JTx1UcfXHMHpsMelxuhk0yrEo'
#    cls.SPREADSHEET_ID = cls.__SPREADSHEET_ID
    '''
    # root@northern-cross.org
    #cls.SPREADSHEET_ID = '1pImzSEHlsrOroaAZToSotel4JJKqkEnXNcKfr8TzHCw'
    '''
    cls.__SAMPLE_RANGE_NAME = 'A2:E'
    cls.__RANGE_NAME = 'A1'
    cls.__MAJOR_DIMENSION = 'ROWS'
#    cls.SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
#    cls.SCOPES = ['https://www.googleapis.com/auth/drive.file']
#    cls.SCOPES = ['https://www.googleapis.com/auth/drive']
    cls.__SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    #cls.kindle_cash_dir = r'C:\Users\ykomi\AppData\Local\Amazon\Kindle\Cache'
    cls.__kindle_cache_file = r'C:\Users\ykomi\AppData\Local\Amazon\Kindle\Cache\KindleSyncMetadataCache.xml'
#    cls.__db_id = 7
    cls.__db_fname_base = r'C:\Users\ykomi\cur\python\kindledb\book'
    cls.__db_file_ext = r'sqlite'
    cls.__db_file = cls.get_db_fname(cls.db_fname_base, cls.db_id, cls.db_file_ext)
    #r'C:\Users\ykomi\cur\python\kindledb\book7.sqlite'
#    cls.db_file = r'C:\Users\ykomi\cur\python\kindledb\book4.sqlite'
    cls.__incsvfile = r"C:\Users\ykomi\cur\python\kindledb\kindle_book_list.csv"
#    cls.incsvfile = r"C:\Users\ykomi\cur\python\kindledb\a.csv"
    cls.__encoding = "utf8"
    cls.__newline = ""
    cls.__incsv_headers = ['ASIN', 'title', 'authors', 'publishers', 'publication_date', 'purchase_date', 'textbook_type', 'cde_contenttype', 'content_type']
    cls.__table_name = "book"
    cls.__table_def_stmt = f"""CREATE TABLE if not exists {cls.table_name} (
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
  '''
  @classmethod
  def get_(cls):
    return cls.
  '''

  @classmethod
  def get_credentials(cls):
    return cls.__credentials

  @property
  def credentials(cls):
    return cls.__credentials

  @property
  def SPREADSHEET_ID(cls):
    return cls.__SPREADSHEET_ID

  @property
  def spreadsheet_id(cls):
    return cls.__SPREADSHEET_ID

  @classmethod
  def get_SCOPES(cls):
    return cls.__SCOPES

  @property
  def SCOPES(cls):
    return cls.__SCOPES

  @property
  def kindle_cache_file(cls):
    print("kindle_cache_file inside ther getter")
    return cls.__kindle_cache_file

  @classmethod
  def get_db_id(cls):
    return cls.__db_id

  
  @classmethod
  def set_db_id(cls, arg):
  #  return cls.__db_id = arg
      Env2.__db_id = arg
  
  db_id = property(get_db_id, set_db_id)
  

  @property
  def db_id_(cls):
    pass

  @db_id_.getter
  def db_id_(cls):
    print("db_id inside ther getter")
    return Integer(cls.__db_id)

  @property
  def db_fname_base(cls):
    pass

  @db_fname_base.getter
  def db_fname_base(cls):
    print("db_fname_base inside ther getter")
    return cls.__db_fname_base

  @property
  def db_file_ext(cls):
    return cls.__db_file_ext
  @property
  def db_file(cls):
    return cls.__db_file
  @property
  def incsvfile(cls):
    return cls.__incsvfile
  @property
  def encoding(cls):
    return cls.__encoding
  @property
  def newline(cls):
    return cls.__newline
  @property
  def incsv_headers(cls):
    return cls.__incsv_headers
  @property
  def table_name(cls):
    return cls.__table_name
  @property
  def table_def_stmt(cls):
    return cls.__table_def_stmt


#  @classmethod
#  def get_SPREADSHEET_ID(cls):
#    return cls.SPREADSHEET_ID

  @classmethod
  def get_SAMPLE_RANGE_NAME(cls):
    return cls.__SAMPLE_RANGE_NAME

  @property
  def SAMPLE_RANGE_NAME(cls):
    return cls.__SAMPLE_RANGE_NAME

  @classmethod
  def get_RANGE_NAME(cls):
    return cls.__RANGE_NAME

  @property
  def RANGE_NAME(cls):
    return cls.__RANGE_NAME

  @classmethod
  def get_MAJOR_DIMENSION(cls):
    return cls.__MAJOR_DIMENSION

  @property
  def MAJOR_DIMENSION(cls):
    return cls.__MAJOR_DIMENSION

  @classmethod
  def get_kindle_cache_file(cls):
    return cls.__kindle_cache_file

  @property
  def kindle_cache_file(cls):
    return cls.__kindle_cache_file

  @classmethod
  def get_db_file(cls):
    return cls.__db_file

  @property
  def db_file(cls):
    return cls.__db_file

  @classmethod
  def get_table_name(cls):
    return cls.__table_name

  @property
  def table_name(cls):
    return cls.__table_name

  @classmethod
  def get_table_def_stmt(cls):
    return cls.__table_def_stmt

  @property
  def table_def_stmt(cls):
    return cls.__table_def_stmt

  @classmethod
  def get_incsv_headers(cls):
    return cls.__incsv_headers

  @property
  def incsv_headers(cls):
    return cls.__incsv_headers

  @classmethod
  def get_incsvfile(cls):
    return cls.incsvfile

  @classmethod
  def get_encoding(cls):
    return cls.encoding

  @classmethod
  def get_newline(cls):
    return cls.newline

if __name__ == '__main__':
    print( Env2.db_id )