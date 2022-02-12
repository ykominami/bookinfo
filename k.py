from env3 import Env3
from kindlelist import KindleList
#import sys

env3 = Env3()
db_fname = env3.get_new_db_fname()
print(db_fname)
print("------")
env3.set_db_fname( db_fname )
kindlelist = KindleList(env3)
#kindlelist.test_csv2db()
#kindlelist.csv2db_bulk_with_dict()
#kindlelist.csv2db_with_dict()
kindlelist.xml2db_with_dict()

#kindlelist.db2gss()
