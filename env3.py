from logging import basicConfig, getLogger, DEBUG
import os
import os.path
#import pyocr
#import pyocr.builders

class Env3:
  def __init__(self):
    # ykominami@gmail.com
    self.logger = getLogger(__name__)
    self.logger.debug('using debug. start running')
    self.logger.debug('finished running')

    self.__credentials = 'client_secret_855711122174-5itvr3iu0fpa5un9fvl6j3f1qu1su19m.apps.googleusercontent.com.json'
#    self.credentials = self.__credentials
  # kindle-list-2022 - Google Sheets
    self.__SPREADSHEET_ID = '1bx2wC_XhNvQOhdNiK1JTx1UcfXHMHpsMelxuhk0yrEo'
#    self.SPREADSHEET_ID = self.__SPREADSHEET_ID
    '''
    # root@northern-cross.org
    #self.SPREADSHEET_ID = '1pImzSEHlsrOroaAZToSotel4JJKqkEnXNcKfr8TzHCw'
    '''
    self.__SAMPLE_RANGE_NAME = 'A2:E'
    self.__RANGE_NAME = 'A1'
    self.__MAJOR_DIMENSION = 'ROWS'
#    self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
#    self.SCOPES = ['https://www.googleapis.com/auth/drive.file']
#    self.SCOPES = ['https://www.googleapis.com/auth/drive']
    self.__SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    #self.kindle_cash_dir = r'C:\Users\ykomi\AppData\Local\Amazon\Kindle\Cache'
    self.__kindle_cache_file = r'C:\Users\ykomi\AppData\Local\Amazon\Kindle\Cache\KindleSyncMetadataCache.xml'
    self.__db_id = 13
    self.__db_fname_base = r'C:\Users\ykomi\cur\python\kindledb\book'
    self.__db_file_ext = r'sqlite'
    self.__db_file = self.get_db_fname(self.db_fname_base, self.db_id, self.db_file_ext)
    #r'C:\Users\ykomi\cur\python\kindledb\book7.sqlite'
#    self.db_file = r'C:\Users\ykomi\cur\python\kindledb\book4.sqlite'
    self.__incsvfile = r"C:\Users\ykomi\cur\python\kindledb\kindle_book_list.csv"
#    self.incsvfile = r"C:\Users\ykomi\cur\python\kindledb\a.csv"
    self.__encoding = "utf8"
    self.__newline = ""
    self.__incsv_headers = ['ASIN', 'title', 'authors', 'publishers', 'publication_date', 'purchase_date', 'textbook_type', 'cde_contenttype', 'content_type']
    self.__table_name = "book"
    self.__table_def_stmt = f"""CREATE TABLE if not exists {self.table_name} (
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

  def get_db_fname(self, db_fname_base, num, ext):
    fn = "%s" % (db_fname_base)
    fn = "%d" % (num)
    fn = "%s%d.%s" % (db_fname_base, num, ext)
    return fn

  def _get_latest_db_fname(self, db_fname_base, num, ext):
    fn = ""
    latest_fn = ""
    while True:
      latest_fn = fn
#      fn = "{}{}.{}".format(db_fname_base, num, ext)
      fn = "%s%d.%s" % (db_fname_base, num, ext)
      if not os.path.exists(fn):
        break
      num += 1

    return latest_fn

  def get_latest_db_fname(self):
    fname_base = self.db_fname_base
    self.logger.debug("fname_base=%s" % (fname_base))
    num = self.db_id
    ext = self.db_file_ext
    return self._get_latest_db_fname(fname_base, num, ext)

  def _get_new_db_fname(self, db_fname_base, num, ext):
    while True:
#      fn = "{}{}.{}".format(db_fname_base, num, ext)
      fn = "%s%d.%s" % (db_fname_base, num, ext)
      if not os.path.exists(fn):
        break
      num += 1

    return fn

  def get_new_db_fname(self):
    fname_base = self.db_fname_base
    self.logger.debug("fname_base=%s" % (fname_base))
    num = self.db_id
    ext = self.db_file_ext
    return self._get_new_db_fname(fname_base, num, ext)

  def _get_new_db_fname(self, db_fname_base, num, ext):
    while True:
#      fn = "{}{}.{}".format(db_fname_base, num, ext)
      fn = "%s%d.%s" % (db_fname_base, num, ext)
      if not os.path.exists(fn):
        break
      num += 1

    return fn

  def set_db_fname(self, db_fname):
    self.__db_file = db_fname

  def get_credentials(self):
    return self.__credentials

  @property
  def credentials(self):
    return self.__credentials

  @property
  def SPREADSHEET_ID(self):
    return self.__SPREADSHEET_ID

  @property
  def spreadsheet_id(self):
    return self.__SPREADSHEET_ID

  @property
  def SCOPES(self):
    return self.__SCOPES

  @property
  def kindle_cache_file(self):
    return self.__kindle_cache_file

  @property
  def db_id(self):
    return self.__db_id

  @db_id.setter
  def db_id(self, arg):
      self.__db_id = arg

  @property
  def db_fname_base(self):
    return self.__db_fname_base

  @property
  def db_file_ext(self):
    return self.__db_file_ext

  @property
  def db_file(self):
    return self.__db_file

  @property
  def incsvfile(self):
    return self.__incsvfile

  @property
  def encoding(self):
    return self.__encoding

  @property
  def newline(self):
    return self.__newline

  @property
  def incsv_headers(self):
    return self.__incsv_headers

  @property
  def table_name(self):
    return self.__table_name

  @property
  def table_def_stmt(self):
    return self.__table_def_stmt

  @property
  def SAMPLE_RANGE_NAME(self):
    return self.__SAMPLE_RANGE_NAME

  @property
  def RANGE_NAME(self):
    return self.__RANGE_NAME

  @property
  def MAJOR_DIMENSION(self):
    return self.__MAJOR_DIMENSION

  @property
  def kindle_cache_file(self):
    return self.__kindle_cache_file

  @property
  def db_file(self):
    return self.__db_file

  @property
  def table_name(self):
    return self.__table_name

  @property
  def table_def_stmt(self):
    return self.__table_def_stmt

  @property
  def incsv_headers(self):
    return self.__incsv_headers

  def get_newline(self):
    return self.newline

if __name__ == '__main__':
  env3 = Env3()
  self.logger.debug( env3.db_id )
