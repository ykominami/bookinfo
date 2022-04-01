from envtarget import EnvTarget

class EnvKindleJSON:
  def __init__(self, db_dir):
    kind = 'kindle'
    self.db_dir = db_dir
    fname_base_kindle = 'kindle'
    db_fname_base_kindle = self.db_dir / fname_base_kindle
    table_columns_default_kindle = ['id']
    table_columns_kindle_book = table_columns_default_kindle
    text_fields_kindle_book = ['title', 'authors']
    text_fields_kindle_progress = []
    text_fields_kindle_purchase = []
    boolean_fields = ['mangaAsin']
    array_to_string_fields_kindle_book = ['authors']
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
      'table_columns':table_columns_kindle_book,
      'text_fields':text_fields_kindle_book,
      'array_to_string_fields':array_to_string_fields_kindle_book,
      'boolean_fields':boolean_fields,
      'id_field':'asin',
      'SPREADSHEET_ID':'1h7HE9S3fzDVa8TclQySC_bokN8v6bGmYL-VrKjm6iXM',
      'SAMPLE_RANGE_NAME':'A2:E',
      'RANGE_NAME':'sheet10!A1:Z',
      'MAJOR_DIMENSION':'ROWS',
      'clear_range':'A1:J',
      'id_related_columns':['id', 'asin'],
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

    self.target = EnvTarget(dict_kindle)

    db = self.target.d['db']
    db['db_file'] = self.target.get_db_fname(
      db['db_fname_base'],
      db['db_id'],
      db['db_file_ext'])
    book = self.target.d['book']
    book['table_def_stmt'] = f"""CREATE TABLE if not exists {book['table_name']} (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      asin STRING UNIQUE,
      webReaderUrl STRING,
      productUrl String,
      title STRING,
      percentageRead INTEGER,
      authors STRING,
      resourceType STRING,
      originType STRING,
      mangaAsin INTEGER
)"""

    purchase = self.target.d['purchase']
    purchase['table_def_stmt'] = f"""CREATE TABLE if not exists {purchase['table_name']} (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      asin STRING UNIQUE,
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
      asin STRING UNIQUE,
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
    (asin, webReaderUrl, productUrl, title, percentageRead, authors, resourceType, originType, mangaAsin)
    VALUES (:asin, :webReaderUrl, :productUrl, :title, :percentageRead, :authors, :resourceType, :originType, :mangaAsin)'''.format(book['table_name'])

    purchase['insert_sql'] = '''INSERT INTO {0}
            ( asin,  ext_id,  purchase_date, year, month, day, year_month, year_month_day)
    VALUES (:asin, :ext_id, :purchase_date, :year, :month, :day, :year_month, :year_month_day)'''.format(self.target.d['purchase']['table_name'])

    progress['insert_sql'] = '''INSERT INTO {0}
            ( asin,  ext_id,  status,  progress_date,  year,  month,  day,  year_month,  year_month_day)
    VALUES (:asin, :ext_id, :status, :progress_date, :year, :month, :day, :year_month, :year_month_day)'''.format(self.target.d['progress']['table_name'])

  def get_new_db_fname(self):
    return self.target.get_new_db_fname()

  def set_db_fname(self, db_fname):
    return self.target.set_db_fname(db_fname)