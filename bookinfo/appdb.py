import sys
from sqlite3 import dbapi2
from bookinfo.sqlite3db import Sqlite3db
from bookinfo.util import Util

# basicConfig(level=DEBUG)  デバッグ時にアンコメント


class AppDb:
    def __init__(self, cmd, db_file, specific_env):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug(
            f"AppDB cmd={cmd} db_file={db_file}using debug. start running"
        )
        self.logger.debug("finished running")

        self.cmd = cmd
        self.db_file = db_file
        self.specific_env = specific_env
        self._db = Sqlite3db(self.cmd, self.db_file, self.specific_env)

        self.logger.debug(f"AppDb.__init__: db_file={db_file}")

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, arg):
        self._db = arg

    def create_table_and_commit(self, key):
        self.logger.debug("AppDb create_table")
        self.db.create_table_and_commit(key)

    def insert_all_and_commit(self, table_name, data_list):
        ret = False
        execute_ret = False
        count = 0
        for dict_rec in data_list:
            try:
                sql = self.specific_env.target.d[table_name]["insert_sql"]
                cursor, execute_ret = self.db.execute(sql, dict_rec)
                count += 1
            except Exception as err:
                self.logger.critical(
                    f"appdb.py 1-1 Exception: {err}"
                )
                self.logger.critical(
                    f"appdb.py 1-2 Exception: {sys.exc_info()[0]}"
                )
                self.logger.critical(f"appdb.py 1-3-a sql: {sql}")
                self.logger.critical(f"appdb.py 1-3-b {execute_ret}")
                execute_ret = False

        if count > 0:
            self.db.commit()
            self.logger.debug("self.db_commit")
            ret = True

        return [ret, count]

    def insert_unique_record_all_and_commit(self, table_name, data_list, key_id):
        ret = False
        count = 0
        execute_ret = True
        for dict_rec in data_list:
            if dict_rec == None:
                continue
            num = dict_rec.get(key_id)
            if num == None:
                continue

            ret = self.select_none(table_name, key_id, num)
            if ret == True:
                execute_ret = True
                try:
                    sql = self.specific_env.target.d[table_name]["insert_sql"]
                    cursor, execute_ret = self.db.execute_statement(sql, dict_rec)
                    count += 1
                except Exception as err:
                    self.logger.critical(
                        f"appdb.py 2-1 Exception: {err}"
                    )
                    self.logger.critical(
                        f"appdb.py 2-2 Exception: {sys.exc_info()[0]}"
                    )
                    self.logger.critical(f"appdb.py 2-3-a sql: {sql}")
                    self.logger.critical(f"appdb.py 2-3-b {dict_rec}")
                    execute_ret = False

        if count > 0:
            self.db.commit()
            self.logger.debug("self.db_commit")
            ret = True

        return [ret, count]

    def select_one_record(self, table_name, key_id, value, specified_num):
        ret = False
        cursor = None
        records = []
        table = self.specific_env.target.d[table_name]
        try:
            sql = f'SELECT * FROM {table["table_name"]} WHERE {key_id} = "{value}"'
            cursor, execute_ret = self.db.execute_statement(sql)
            if (execute_ret == True) & (cursor != None):
                records = cursor.fetchall()
                size = len(records)
                if size == specified_num:
                    ret = True
        except Exception as err:
            self.logger.critical(f"appdb.py 3 Exception: {err}")
            self.logger.critical(
                f"appdb.py 3-1 Exception: {sys.exc_info()[0]}"
            )

        return [ret, records]

    def select_one(self, table_name, value):
        ret, records = self.select_one_record(table_name, value, 1)
        return ret

    def select_none(self, table_name, key_id, value):
        ret, records = self.select_one_record(table_name, key_id, value, 0)
        return ret

    def select_all_as_dict(self, table_name, list):
        cursor = None
        ret = False
        table = self.specific_env.target.d[table_name]

        try:
            sql = f"SELECT * FROM {table_name}"
            cursor, execute_ret = self.db.execute_statement(sql)
            if (execute_ret == True) & (cursor != None):
                columns = None
                for r in cursor.fetchall():
                    if columns == None:
                        columns = r.keys()
                    list.append({x: r[x] for x in columns})
                ret = True
        except Exception as err:
            self.logger.critical(f"appdb.py 4 Exception: {err}")
            self.logger.critical(
                f"appdb.py 4-2 Exception {sys.exc_info()[0]}"
            )

        return ret

    def select_all(self, table_name, list, columns=None):
        cursor = None
        ret = False
        table = self.specific_env.target.d[table_name]

        try:
            if columns == None:
                sql = f"SELECT * FROM {table_name}"
            else:
                columns_str = ",".join(columns)
                sql = f"SELECT {columns_str} FROM {table_name}"

            self.logger.debug("sql=%s" % sql)
            cursor, execute_ret = self.db.execute_statement(sql)
            self.logger.debug(f"execute_ret={execute_ret}")
            self.logger.debug(f"cursor={cursor}")
            if (execute_ret == True) & (cursor != None):
                self.logger.debug("appdb select_all")
                for r in cursor.fetchall():
                    if columns == None:
                        list.append([r.values()])
                    else:
                        list.append([r[x] for x in columns])
                ret = True
        except Exception as err:
            self.logger.critical(f"appdb.py 5 Exception: {err}")
            self.logger.critical(
                f"appdb.py 5-2 Exception: {sys.exc_info()[0]}"
            )

        return ret

    def close(self):
        self.db.close()

    def convert_boolean_to_integer(self, nary, boolean_fields=[]):
        self.db.convert_boolean_to_integer(nary, boolean_fields)

    def convert_integer_to_boolean(self, nary, boolean_fields=[]):
        self.db.convert_integer_to_boolean(nary, boolean_fields)
