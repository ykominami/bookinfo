from logging import basicConfig, getLogger, DEBUG
import os
#import os.path
from pathlib import Path
#import pyocr
#import pyocr.builders
from kindlelist import KindleList
from kindlejson import KindleJSON
from calibrex import Calibrex
from bookstore import Bookstore

from envkindlejson import EnvKindleJSON
from envkindlelist import EnvKindleList
from envcalibre import EnvCalibre
from envbookstore import EnvBookstore
class Env3:
  @property
  def calibre(self):
    return self.__calibre
  @calibre.setter
  def calibre(self, value):
    self.__calibre = value

  def __init__(self):
    # ykominami@gmail.com
    self.logger = getLogger(__name__)
    self.logger.debug('using debug. start running')
    self.logger.debug('finished running')

    self.d = {}
    self.d['klass'] = { 'kindle':KindleList, 'kindlelist':KindleList, 'kindlejson':KindleJSON, 'calibre':Calibrex, 'bookstore':Bookstore }
    #self.d['calibre'] = init_calibre()
    self.d['gcp'] = {}
    self.d['gcp']['credentials'] = 'client_secret_855711122174-5itvr3iu0fpa5un9fvl6j3f1qu1su19m.apps.googleusercontent.com.json'
    #self.d['gcp']['token'] = 'token.json'
    self.d['gcp']['token'] = 'token.pickle'
    self.d['gcp']['SCOPES'] = ['https://www.googleapis.com/auth/spreadsheets']
    self.db_dir = Path( r'C:\Users\ykomi\cur\python\kindledb' )

    self.d['kindlejson'] = EnvKindleJSON(self.db_dir)
    #self.d['kindlelist'] = EnvKindleList(self.db_dir)
    #self.d['kindle'] = self.init_kindle()
    # self.d['calibre'] = self.init_calibre()
    self.d['calibre'] = EnvCalibre(self.db_dir)

    self.d['bookstore'] = {}
    year_range = range(2014, 2023)
    for y in year_range:
      year = "{}".format(y)
      #self.d['bookstore'][year] = self.init_bookstore(year)
      self.d['bookstore'][year] = EnvBookstore(year, self.db_dir)


if __name__ == '__main__':
  env3 = Env3()
  self.logger.debug( env3.db_id )
