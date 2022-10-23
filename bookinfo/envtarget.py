from pathlib import Path
from bookinfo.util import Util

class EnvTarget:
    @property
    def d(self):
        return self.__d

    @d.setter
    def d(self, value):
        self.__d = value

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        self.__target = value

    @property
    def db_dir_path(self):
        return self.__db_dir_path

    @db_dir_path.setter
    def db_dir_path(self, value):
        self.__db_dir_path = value

    def __init__(self, db_dir, dictx):
        self.logger = Util.getLoggerx("EnvTarget")
        self.logger.debug("EnvTarget using debug. start running")
        self.logger.debug("EnvTarget finished running")

        self.__db_dir_path = Path(db_dir)
        self.__d = dictx
        self.__target = None

    def _make_filename(self, fname_base, num, ext):
        fn = f"{fname_base}_{num}.{ext}"
        return fn

    def _get_latest_db_fname(self, fname_base, num, ext):
        fn = ""
        db_path = None
        prev_path = None
        latest_path = None
        while True:
            fn = self._make_filename(fname_base, num, ext)
            db_path = self.db_dir_path / fn
            self.logger.debug(f"EnvTarget _get_latestdb_fname db_path={db_path}")
            if db_path.exists():
                self.logger.debug(
                    f"EnvTarget _get_latestdb_fname EXIST db_path={db_path}"
                )
                prev_path = db_path
            else:
                self.logger.debug(
                    f"EnvTarget _get_latestdb_fname NOT EXIST db_path={db_path}"
                )
                latest_path = prev_path
                break
            num += 1

        self.logger.debug(f"EnvTarget _get_latestdb_fname latest_path={latest_path}")
        return latest_path

    def get_latest_db_fname(self):
        db = self.__d["db"]
        fname_base = db["db_fname_base"]
        self.logger.debug("EnvTarget get_latest_db_fname fname_base=%s" % (fname_base))
        num = db["db_id"]
        ext = db["db_file_ext"]
        return self._get_latest_db_fname(fname_base, num, ext)

    def get_latest_db_fname_with_year(self, year):
        db = self.__d["db"]
        fname_base = "_".join( [db["db_fname_base"], str(year)] )
        self.logger.debug("EnvTarget get_latest_db_fname fname_base=%s" % (fname_base))
        num = db["db_id"]
        ext = db["db_file_ext"]
        return self._get_latest_db_fname(fname_base, num, ext)

    def _get_new_db_fname(self, fname_base, num, ext):
        while True:
            fn = self._make_filename(fname_base, num, ext)
            db_path = self.db_dir_path / fn
            if not db_path.exists():
                break
            num += 1

        return db_path

    def get_new_db_fname(self):
        db = self.__d["db"]
        fname_base = db["db_fname_base"]
        self.logger.debug("fname_base=%s" % (fname_base))
        num = db["db_id"]
        ext = db["db_file_ext"]
        new_db_fname = self._get_new_db_fname(fname_base, num, ext)
        self.logger.debug(f"new_db_fname={new_db_fname}")
        return new_db_fname

    def get_new_db_fname_with_year(self, year):
        db = self.__d["db"]
        fname_base = "_".join( [db["db_fname_base"], str(year)] )
        self.logger.debug("fname_base=%s" % (fname_base))
        num = db["db_id"]
        ext = db["db_file_ext"]
        new_db_fname = self._get_new_db_fname(fname_base, num, ext)
        self.logger.debug(f"new_db_fname={new_db_fname}")
        return new_db_fname
