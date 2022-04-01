from envtarget import EnvTarget

class EnvKindleList:
  def __init__(self, db_dir):
    kind = 'kindle'
    self.db_dir = db_dir
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

    obj = EnvTarget(dict_kindle)

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

    self.obj = obj
