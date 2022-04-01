from envtarget import EnvTarget
import json

class EnvBase:
  def __init__(self, year, db_dir):
    kind = 'bookstore'
    self.db_dir = db_dir
    fname_base_bookstore = '{}_{}'.format(kind, year)
    db_fname_base_bookstore = self.db_dir / fname_base_bookstore

    fname = "a.json"
    from_json = json.loads(open(fname))

    table_columns_default_bookstore = from_json['table_columns_default_bookstore']
    table_columns_bookstore_book = table_columns_default_bookstore
    text_fields_bookstore_book = from_json['text_fields_bookstore_book']
    text_fields_bookstore_purchase = from_json['text_fields_bookstore_purchase']
    text_fields_bookstore_progress = from_json['text_fields_bookstore_progress']

    spreadsheet_ids = from_json['spreadsheet_ids']
    dict_bookstore_db = from_json['dict_bookstore_db']
    dict_bookstore_db['db_fname_base'] = db_fname_base_bookstore
    dict_bookstore_book = from_json['dict_bookstore_book']
    dict_bookstore_book['table_columns'] = table_columns_bookstore_book
    dict_bookstore_book['text_fields'] = text_fields_bookstore_book
    dict_bookstore_book['SPREADSHEET_ID'] = spreadsheet_ids[year]
    dict_bookstore_purchase = from_json['dict_bookstore_purchase']
    dict_bookstore_purchase['table_columns'] = table_columns_bookstore_purchase
    dict_bookstore_purchase['text_fields'] = text_fields_bookstore_purchase
    dict_bookstore_purchase['SPREADSHEET_ID'] = spreadsheet_ids[year]
    dict_bookstore_progress = from_json['dict_bookstore_progress']
    dict_bookstore_progress['text_fields'] = text_fields_bookstore_purchase
    dict_bookstore_progress['SPREADSHEET_ID'] = spreadsheet_ids[year]
    '''
    table_columns_default_bookstore = ['id']
    text_fields_bookstore_book = ['xid', 'asin', 'title', 'authors', 'publishers', 'publication_date', 'purchase_date', 'read_status', 'shape', 'category']
    text_fields_bookstore_purchase = []
    text_fields_bookstore_progress = []
    spreadsheet_ids = {
      2014:'1C5AW-QPwJoMn9NcKRZMIScO5fB63KbWKiO2XE0kHDSc',
      2015:'1aE_ckhR6jqdF233vLJ124MFzSUsB7m_dWguKg4NEQFU',
      2016:'1ABSIIio25bDy3_jNZWkuKs4yUNGBDfuY_k9trl0IpW0',
      2017:'1BQVRjVGqw98aaQZ24ZXnTFw9cVOn07r-LFKI2gPK_0Y',
      2018:'113anNUwziaOobJQCgfJJrhTPdgRLAfplXrDfhoSkcq0',
      2019:'1F4zFRKTnX2G4Ffd83_BAZotSIXk6L9u7diSgCD-XW5k',
      2020:'1r0VK42-ZRMVqkIrED1O_xR8ap-uWBKkPD6tPTZvzE_E',
      2021:'1ShcCrP8x3V3XC028dvZjirMLY0c1Gj4Qc1U1vBn6Uu4',
      2022:'1JAqTpaLFUJX1m5GCFRCKaKARMDJkPxZkFvGPvWT3Jsc',
    }
    dict_bookstore_db = {
      'db_id':0,
      'db_fname_base':db_fname_base_bookstore,
      'db_file_ext':r'sqlite',
      'encoding':'utf_8_sig',
      'newline':"",
    }
    dict_bookstore_book = {
      'table_name':'book',
      'table_columns':table_columns_bookstore_book,
      'text_fields':text_fields_bookstore_book,
      'id_field':'asin',
      'SPREADSHEET_ID':spreadsheet_ids[year],
      'SAMPLE_RANGE_NAME':'A2:E',
      'RANGE_NAME':'sheet10!A1:Z',
      'MAJOR_DIMENSION':'ROWS',
      'clear_range':'A1:J',
      'id_related_columns':['id', 'asin'],
    }
    dict_bookstore_purchase = {
      'table_name':'purchase',
      'text_fields':text_fields_bookstore_purchase,
      'id_field':'ext_id',
      'SPREADSHEET_ID':spreadsheet_ids[year],
      'SAMPLE_RANGE_NAME':'A2:E',
      'RANGE_NAME':'A1',
      'MAJOR_DIMENSION':'ROWS',
      'clear_range':'A1:J',
    }
    dict_bookstore_progress = {
      'table_name':'progress',
      'text_fields':text_fields_bookstore_progress,
      'SPREADSHEET_ID':spreadsheet_ids[year],
    }

    '''

    #  'kindle_cache_file':r'C:\Users\ykomi\AppData\Local\Amazon\Kindle\Cache\KindleSyncMetadataCache.xml',


    dict_bookstore= {
      'db':dict_bookstore_db,
      'book':dict_bookstore_book,
      'purchase':dict_bookstore_purchase,
      'progress':dict_bookstore_progress,
    }

    obj = EnvTarget(dict_bookstore)
    db = obj.d['db']

    db['db_file'] = obj.get_db_fname(
      db['db_fname_base'],
      db['db_id'],
      db['db_file_ext'])

    book = obj.d['book']
    book['table_def_stmt'] = f"""CREATE TABLE if not exists {book['table_name']} (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      xid INTEGER UNIQUE,
      bookstore STRING,
      title STRING,
      asin STRING,
      authors STRING,
      publishers STRING,
      publication_date TEXT,
      purchase_date TEXT,
      read_status INTEGER,
      shape INTEGER,
      category STRING
)"""
    purchase = obj.d['purchase']
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

    progress = obj.d['progress']
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
            (xid,  bookstore,  title,  asin,  authors,  publishers,  publication_date,  purchase_date,  read_status,  shape,  category)
    VALUES (:xid, :bookstore, :title, :asin, :authors, :publishers, :publication_date, :purchase_date, :read_status, :shape, :category)'''.format(book['table_name'])

    purchase['insert_sql'] = '''INSERT INTO {0}
            ( asin,  ext_id,  purchase_date, year, month, day, year_month, year_month_day)
    VALUES (:asin, :ext_id, :purchase_date, :year, :month, :day, :year_month, :year_month_day)'''.format(obj.d['purchase']['table_name'])

    progress['insert_sql'] = '''INSERT INTO {0}
            ( asin,  ext_id,  status,  progress_date,  year,  month,  day,  year_month,  year_month_day)
    VALUES (:asin, :ext_id, :status, :progress_date, :year, :month, :day, :year_month, :year_month_day)'''.format(obj.d['progress']['table_name'])

    self.obj = obj
