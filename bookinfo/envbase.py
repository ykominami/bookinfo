import json
from pathlib import Path
import string
import re
from bookinfo.envtarget import EnvTarget
from bookinfo.util import Util

class EnvBase:
    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        self.__target = value

    def __init__(self, db_dir, kind):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("EnvBase using debug. start running")
        self.logger.debug("EnvBase finished running")
        self.kind = kind
        self.db_dir = db_dir

        config_path = Path("config") / self.kind
        default_path = config_path / "default.json"
        second_path = config_path / "second.json"
        x_path = config_path / "x.json"
        sql_path = config_path / "sql.txt"

        self.vars_dict = {}
        self.logger.debug(self.vars_dict.keys())
        self.logger.debug("\n".join(self.vars_dict.keys()))
        with open(default_path, "r", encoding="utf-8") as f:
            self.vars_dict = json.load(f)
            self.logger.debug("1")
            self.logger.debug(self.vars_dict.keys())
            self.logger.debug("\n".join(self.vars_dict.keys()))
        with open(second_path, "r", encoding="utf-8") as f:
            result = string.Template(f.read()).substitute(self.vars_dict)
            result = result.replace("'", '"')
            dictx = json.loads(result)
            self.vars_dict = self.vars_dict | dictx
            self.logger.debug("2")
            self.logger.debug(self.vars_dict.keys())
            self.logger.debug("\n".join(self.vars_dict.keys()))
        with open(x_path, "r", encoding="utf-8") as f:
            self.logger.debug(f"x_path={x_path}")
            dictx = json.load(f)
            self.vars_dict = self.vars_dict | dictx
            self.logger.debug("3")
            self.logger.debug(self.vars_dict.keys())
            self.logger.debug("\n".join(self.vars_dict.keys()))

        self.logger.debug("4")
        self.logger.debug(self.vars_dict.keys())
        self.logger.debug("41")
        self.get_sql_dict(sql_path, self.vars_dict)

        self.logger.debug("42")
        self.logger.debug(self.vars_dict.keys())
        self.logger.debug("\n".join(self.vars_dict.keys()))

        # self.target = EnvTarget(db_dir, self.vars_dict)
        self.__target = EnvTarget(db_dir, self.vars_dict)
        # targetx = self.target()
        db = self.__target.d["db"]
        db["db_fname_base"] = self.kind

        # tables = ['book', 'purchase', 'progress']
        for table in db["tables"]:
            for sql_index in db["sql_indexes"]:
                self.target.d[table][sql_index] = self.vars_dict[table][sql_index]

    # def set_db_fname(self, db_fname):
    #  self.vars_dict['db']['db_file'] = db_fname

    # def get_db_fname(self):
    #  return self.vars_dict['db']['db_file']

    def get_db_file(self):
        return self.vars_dict["db"]["db_file"]

    def set_db_file(self, filename):
        self.vars_dict["db"]["db_file"] = filename

    def make_filename_base(self, delimitor, *args):
        str_list = list(map(str, args))
        return delimitor.join(str_list)

    def make_filename(self, filename_base, ext):
        fn = "%s.%s" % (filename_base, ext)
        return fn

    def make_db_filenamebase(self):
        filename_base = self.make_filename_base(
            "_", self.vars_dict["db"]["db_fname_base"], self.vars_dict["db"]["db_id"]
        )
        return filename_base

    def get_db_name(self):
        return self.vars_dict["db"]["db_file"]

    def set_db_name(self, db_dir_path):
        filename_base = self.make_db_filenamebase()
        db_file = self.make_filename(filename_base, self.vars_dict["db"]["db_file_ext"])
        self.vars_dict["db"]["db_file"] = db_dir_path / db_file

    def get_sql_dict(self, sql_file_path, dictx):
        with open(sql_file_path, "r") as f:
            content = f.read()
            ary = content.splitlines()
            kind = None
            sql_index = None
            for l in ary:
                if re.match("^#", l):
                    xary = l.split()
                    if len(xary) < 3:
                        raise

                    self.logger.debug(xary)
                    if kind is not None and sql_index is not None:
                        self.logger.debug("A 0")
                        dictx[kind][sql_index] = "\n".join(dictx[kind][sql_index])

                    kind = xary[1]
                    sql_index = xary[2]
                    self.logger.debug(f"kind={kind}")
                    self.logger.debug(f"sql_index={sql_index}")
                    if kind is None or sql_index is None:
                        raise
                    if kind not in dictx.keys():
                        self.logger.debug("A 1")
                        dictx[kind] = {}

                    if dictx[kind] is None:
                        self.logger.debug("A 2")
                        dictx[kind] = {}

                    if sql_index not in dictx[kind].keys():
                        self.logger.debug("A 3")
                        dictx[kind][sql_index] = []

                    if dictx[kind][sql_index] is None:
                        self.logger.debug("A 4")
                        dictx[kind][sql_index] = []

                elif kind != None and sql_index != None:
                    self.logger.debug(f"kind={kind}")
                    self.logger.debug(f"sql_index={sql_index}")
                    self.logger.debug(dictx[kind])
                    dictx[kind][sql_index].append(l)
                else:
                    raise

            self.logger.debug(f"{dictx.keys()}")
            dictx[kind][sql_index] = "\n".join(dictx[kind][sql_index])

        return dictx

    def get_new_db_fname(self):
        return self.target.get_new_db_fname()

    def get_new_db_fname_with_year(self, year):
        return self.target.get_new_db_fname_with_year(year)

    def get_latest_db_fname(self):
        return self.target.get_latest_db_fname()

    def get_latest_db_fname_with_year(self, year):
        return self.target.get_latest_db_fname_with_year(year)
