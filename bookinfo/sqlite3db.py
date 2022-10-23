import sqlite3
from pathlib import Path
import os
from bookinfo.util import Util

class Sqlite3db:
    def __init__(self, cmd, db_file, specific_env):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("using debug. start running")
        self.logger.debug("finished running")

        self.sqlite3 = sqlite3
        self.db_file = db_file
        self.specific_env = specific_env

        self.conn = None
        self.cursor = None
        self.valid_db = False
        path = Path(db_file)
        if cmd == "CREATE":
            self.init_for_create(path)
        else:
            self.init_for_update(path)
            #
        self.connect()

    def init_for_create(self, path):
        if not path.exists():
            self.valid_db = True

    def init_for_update(self, path):
        if path.exists():
            statinfo = os.stat(path)
            if statinfo.st_size > 0:
                self.valid_db = True

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def connect(self):
        self.logger.debug("sqlite3db.py connect=")
        self.logger.debug(self.conn)
        self.logger.debug("self.db_file=%s" % (self.db_file))

        if self.conn == None:
            self.logger.debug(self.db_file)
            self.conn = sqlite3.connect(
                self.db_file,
                check_same_thread=False,
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            )
            sqlite3.dbapi2.converters["DATETIME"] = sqlite3.dbapi2.converters[
                "TIMESTAMP"
            ]
            # self.conn.row_factory = sqlite3.Row
            self.conn.row_factory = self.dict_factory
            self.logger.debug(f"sqlite3db.py connect None -> conn={self.conn}")

    def create_table_and_commit(self, table_name):
        self.create_table(table_name)
        # データベースへコミット。これで変更が反映される。
        self.conn.commit()

    def create_table(self, table_name):
        ret = False
        cursor = self.get_cursor()
        try:
            sql = self.specific_env.target.d[table_name]["table_def_stmt"]
            cursor.execute(sql)
            ret = True
        except self.sqlite3.OperationalError as err:
            self.logger.critical(
                f"Sqlite3db create_table sqlite3.OperationalError: {err}"
            )

        return [cursor, ret]

    def get_cursor(self):
        if self.cursor == None:
            self.cursor = self.conn.cursor()

        return self.cursor

    def execute_statement_x(self, statement, varlist):
        ret = False
        cursor = self.get_cursor()

        try:
            cursor.execute(statement, varlist)
        except self.sqlite3.IntegrityError as err:
            self.logger.critical(
                f"Sqlite3db execute_statement_x sqlite3.IntegrityError: {err}"
            )
            self.logger.critical( f"statement={statement}")
            self.logger.critical( f"varlist={varlist}")
        except self.sqlite3.ProgrammingError as err:
            self.logger.critical(
                f"Sqlite3db execute_statement_x sqlite3.ProgrammingError: {err}"
            )
            self.logger.critical( f"statement={statement}")
            self.logger.critical( f"varlist={varlist}")

        return [cursor, ret]

    def execute_statement(self, statement, varlist=None):
        ret = False
        cursor = self.get_cursor()

        try:
            if varlist == None:
                cursor.execute(statement)
                ret = True
            else:
                cursor.execute(statement, varlist)
                ret = True
        except self.sqlite3.IntegrityError as err:
            self.logger.critical(
                f"Sqlite3db execute_statement sqlite3.IntegrityError: {err}"
            )
            self.logger.critical( f"statement={statement}")
            self.logger.critical( f"varlist={varlist}")
        except sqlite3.OperationalError as err:
            self.logger.critical(
                f"Sqlite3db execute_statement sqlite3.OperationalError: {err}"
            )
            self.logger.critical( f"statement={statement}")
            self.logger.critical( f"varlist={varlist}")
        except self.sqlite3.ProgrammingError as err:
            self.logger.critical(
                f"Sqlite3db execute_statement sqlite3.ProgrammingError: {err}"
            )
            self.logger.critical( f"statement={statement}")
            self.logger.critical( f"varlist={varlist}")
        except Exception as err:
            self.logger.critical(
                f"Sqlite3db execute_statement Exception: {err}"
            )
            self.logger.critical( f"statement={statement}")
            self.logger.critical( f"varlist={varlist}")

        return [cursor, ret]

    def execute_and_commit(self, statement):
        ret = False
        cursor = self.get_cursor()
        try:
            cursor.execute(statement)
            self.conn.commit()
            ret = True
        except self.sqlite3.IntegrityError as err:
            self.logger.critical(
                f"Sqlite3db execute_and_commit sqlite3.IntegrityError: {err}"
            )

        return [cursor, ret]

    def commit(self):
        self.conn.commit()

    def close_cursor(self):
        if self.cursor != None:
            try:
                self.cursor.close()
            except self.sqlite3.ProgrammingError as err:
                self.logger.critical(
                    f"Sqlite3db close_cursor sqlite3.ProgrammingError: {err}"
                )

            self.cursor = None

    def close_conn(self):
        if self.conn != None:
            self.conn.close()
            self.conn = None

    def close(self):
        self.close_cursor()
        self.close_conn()

    def show_nary_boolean(self, nary, boolean_fields):
        for dict in nary:
            for bf in boolean_fields:
                self.logger.debug(f"0 h={bf} keys={dict.keys()}")
                if bf in dict.keys():
                    self.logger.debug(f"1 h={bf}")
                    if dict[bf] != None:
                        self.logger.debug(f"2 {dict[bf]}")

    def convert_boolean_to_integer(self, nary, boolean_fields=[]):
        for dict in nary:
            for h in boolean_fields:
                if h in dict.keys():
                    if dict[h] != None:
                        if dict[h]:
                            dict[h] = 1
                        else:
                            dict[h] = 0

        # self.show_nary_boolean(nary, boolean_fields)

    def convert_integer_to_boolean(self, nary, boolean_fields=[]):
        for dict in nary:
            for h in boolean_fields:
                if h in dict.keys():
                    if dict[h] != None:
                        if dict[h] == 1:
                            dict[h] = True
                        else:
                            dict[h] = False
