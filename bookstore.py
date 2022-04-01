from logging import basicConfig, getLogger, DEBUG
from appbase import AppBase
from util import Util

class Bookstore(AppBase):
  def __init__(self, target_env, env_gcp, cmd):
    self.logger = getLogger(__name__)
    self.logger.debug('Bookstore using debug. start running')
    self.logger.debug('Bookstore finished running')

    super().__init__(target_env, env_gcp, cmd)

  def cmd_update(self, target_name, target, year):
    self.logger.debug("update table {}".format(target_name))
    db_fname = target.get_latest_db_fname()
    self.logger.debug(db_fname)
    self.logger.debug("------")
    target.set_db_fname( db_fname )
    #inst = Calibrex(target, CMD)
    nary = []
    range=None
    range_val = 'Sheet1!A1:L'
    ranges = range_val
    response = self.get_gss('book', ranges=ranges)
    book_fname = "book-{}.json".format(year)
    Util.json2file(response, book_fname)

    listx = []
    ret = self.get_id_from_db('book', listx)
    dictx = { x[1]:x[0] for x in listx }
    nary_purchase = self.dictarray_for_purchase(nary, dictx)
    self.dictarray2db('purchase', nary_purchase)
    nary_purchase = [ it for it in nary_purchase if it.get('purchase_date', None) != None ]
    self.dictarray2db('purchase', nary_purchase)
    self.db2gss_update('purchase')

    self.db2gss_update('progress')
