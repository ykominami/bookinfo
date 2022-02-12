from env2 import Env2
from kindlelist import KindleList
#import sys

Env2.init()
kindlelist = KindleList(Env2)
#kindlelist.test_csv2db()
#kindlelist.csv2db_bulk_with_dict()
#kindlelist.csv2db_with_dict()
kindlelist.xml2db_with_dict()

#kindlelist.db2gss()
