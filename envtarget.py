from logging import basicConfig, getLogger, DEBUG
import os

class EnvTarget:
  @property
  def d(self):
    return self.__d

  @d.setter
  def d(self, value):
    self.__d = value

  def __init__(self, dictx):
    self.logger = getLogger("EnvTarget")
    self.logger.debug('using debug. start running')
    self.logger.debug('finished running')

    self.d = dictx

  def get_db_fname(self, db_fname_base, num, ext):
    fn = "%s_%d.%s" % (db_fname_base, num, ext)
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
    new_db_fname = self._get_new_db_fname(fname_base, num, ext)
    print("new_db_fname={}".format(new_db_fname))
    return new_db_fname

  def set_db_fname(self, db_fname):
    db = self.d['db']
    db['db_file'] = db_fname
