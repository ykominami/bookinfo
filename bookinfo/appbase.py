from abc import ABC, ABCMeta, abstractmethod
import copy
import pprint
from turtle import end_fill

from bookinfo.appdb import AppDb
from bookinfo.util import Util

from bookinfo.googleapiclientx import GoogleApiClientx
from bookinfo.credential import Credential


# class AppBase(metaclass=ABCMet):
class AppBase(ABC):
    BOOK = 'book'
    PURCHASE = 'purchase'
    PROGRESS = 'progress'

    def __init__(self, specific_env, env_gcp, cmd):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("using debug. start running")
        self.logger.debug("finished running")
        self.pickle_dir_name = "pickles"
        self.pickle_ext_name = "pickle"
        self.pp = pprint.PrettyPrinter(indent=4)


        self.specific_env = specific_env
        self.cmd = cmd
        db_file = specific_env.get_db_file()
        self.appdb = AppDb(
            self.cmd,
            db_file,
            self.specific_env,
        )
        db = specific_env.target.d["db"]
        self.encoding = db["encoding"]
        self.newline = db["newline"]
        self.table_env = {}
        self.credential = Credential(env_gcp)

        self.names = [self.BOOK, self.PURCHASE, self.PROGRESS]
        self.dict_filename = {}

    def make_pickle_filename(self, target_name, ext_name):
        return f"{target_name}.{ext_name}"

    def make_json_filename(self, basename):
        return f"{basename}.json"

    def register_data(self, parsed):
        if parsed == None:
            return
        ary = parsed["values"]
        headers = ary.pop(0)
        headers[0] = "id"
        index = 0
        inds = []
        for i, j in enumerate(headers):
            if j == "":
                inds.append(i)

        inds_2 = copy.copy(inds)
        inds_2.reverse()
        r_inds = inds_2
        for ind in r_inds:
            del headers[ind]

        new_list = []
        for x in ary:
            length = len(x)
            for ind in r_inds:
                if ind < length:
                    del x[ind]
            new_list.append(x)
        x = [{k: v for k, v in zip(headers, line)} for line in ary]
        self.dictarray2db(self.BOOK, x, "xid")

    def create_tables(self, configx):
        self.create_one_table(self.BOOK)
        self.create_one_table(self.PURCHASE)
        self.create_one_table(self.PROGRESS)

    def create_one_table(self, key):
        self.appdb.create_table_and_commit(key)

    def update_table_purchase_and_progress(self, value_input_option, clear_flag=True):
        table_name = self.BOOK
        list = []
        ret = self.get_id_from_db(table_name, list)
        # id, asin, purchase_date
        id_purchase_date_list = [ x for x in list ]
        nary_purchase = self.dictarray_for_purchase(id_purchase_date_list)
        nary_purchase = [
            it for it in nary_purchase if it != None
        ]
        self.dictarray2db(self.PURCHASE, nary_purchase)
        res_path_purchase = self.dict_filename[self.PURCHASE]

        data = {}
        Util.factory(data)
        self.db2gss_update(res_path_purchase, self.PURCHASE, value_input_option, clear_flag)

        nary_progress = self.dictarray_for_progress(id_purchase_date_list)
        nary_progress = [
            it for it in nary_progress if it != None
        ]
        self.dictarray2db(self.PROGRESS, nary_progress)
        res_path_progress = self.dict_filename[self.PROGRESS]

        data = {}
        Util.factory(data)
        self.db2gss_update(res_path_progress, self.PROGRESS, value_input_option, clear_flag)

    @abstractmethod
    def cmd_update(self, target_name, target):
        raise NotImplementedError("not implement make_progress_table_record")

    def dictarray2db(self, table_name, nary, key_id=None):
        tablex = self.specific_env.target.d[table_name]
        text_fields = tablex.get("text_fields", [])
        array_to_string_fields = self.specific_env.target.d[table_name].get(
            "array_to_string_fields", []
        )
        Util.escape_single_quote_all(nary, text_fields, array_to_string_fields)
        boolean_fields = self.specific_env.target.d[table_name].get(
            "boolean_fields", []
        )
        self.appdb.convert_boolean_to_integer(nary, boolean_fields)
        if key_id is None:
            key_id = tablex.get("id_field", None)
   
        ret, count = self.appdb.insert_unique_record_all_and_commit(
            table_name, nary, key_id
        )
        self.logger.debug(f"In dictarray2db table_name={table_name} ret={ret} count={count}")

        return ret

    def db_close(self):
        self.appdb.close()

    def get_googleapiclientx(self, table_name):
        self.logger.debug(f"appbase.py | get_googleapiclientx table_name={table_name} 1")
        gac = self.table_env.get(table_name, None)
        if not gac:
            self.logger.debug(f"appbase.py | get_googleapiclientx table_name={table_name} 2")
            table_env = self.specific_env.target.d[table_name]
            gac = GoogleApiClientx(table_env, self.credential)
            self.table_env[table_name] = gac
        return gac

    def db2gss_append(self, table_name, clear_flag=False):
        # raise NotImplementedError("not implement db2gss_append")

        listx = []
        ret = self.appdb.select_all_as_dict(table_name, listx)
        return ret

    def db2gss_batchUpdate2(self, res_path, table_name, clear_flag=False):
        self.logger.debug("appbase.py | db2gss_batchUpdate2")
        # exit(0)
        listx = []
        requests = []
        ret = self.appdb.select_all_as_dict(table_name, listx)
        if ret and len(listx) > 0:
            self.logger.debug("db2gss_batchUpdate")
            gac = self.get_googleapiclientx(table_name)
            if gac:
                #            "sheetId": self.specific_env.target.d[table_name]['SPREADSHEET_ID'],
                requests.append(
                    {
                        "updateBorders": {
                            "range": {
                                "sheetId": 0,
                                "startRowIndex": 0,
                                "endRowIndex": 1,
                                "startColumnIndex": 0,
                                "endColumnIndex": 2,
                            },
                            "bottom": {
                                "style": "SOLID",
                                "width": "1",
                                "color": {"red": 0, "green": 0, "blue": 0},
                            },
                        },
                    }
                )
                #     "sheetId": self.specific_env.target.d[table_name]['SPREADSHEET_ID'],

                requests.append(
                    {
                        "repeatCell": {
                            "range": {
                                "sheetId": 0,
                                "startRowIndex": 0,
                                "endRowIndex": 1,
                                "startColumnIndex": 0,
                                "endColumnIndex": 2,
                            },
                            "cell": {
                                "userEnteredFormat": {
                                    "horizontalAlignment": "LEFT",
                                    "textFormat": {
                                        "fontSize": 11,
                                        "bold": True,
                                        "foregroundColor": {
                                            "red": 1.0,
                                        },
                                    },
                                }
                            },
                            "fields": "userEnteredFormat(textFormat,horizontalAlignment)",
                        },
                    }
                )

                body = {"requests": requests}
                gac.upload2gss_batchUpdate_with_body(res_path, body, clear_flag)
                value_input_option = "USER_ENTERED"

    def db2gss_update(self, res_path, table_name, value_input_option, clear_flag=False):
        data = {}
        Util.factory(data)
        filename = data['filename']
        lineno = data['lineno']
        self.logger.debug(f"appbase.py | db2gss_update table_name={table_name} 0 {filename} {lineno}")
        listx = []
        listy = []
        ret = self.appdb.select_all_as_dict(table_name, listx)
        # if ret and len(listx) > 0:
        if ret and len(listx) > 0:
            self.logger.debug("appbase.py | db2gss_update 2")
            listy.append(list(listx[0].keys()))

            for item in listx:
                listy.append(list(item.values()))
            gac = self.get_googleapiclientx(table_name)
            self.logger.debug(f"appbase.py | db2gss_update 3a table_name={table_name}")
            if gac:
                self.logger.debug("appbase.py | db2gss_update 4")
                gac.upload2gss_update_with_body(
                    res_path, listy, value_input_option, clear_flag
                )
            else:
                self.logger.critical("appbase.py | db2gss_update 2")
        else:
            self.logger.debug("appbase.py | db2gss_update 5")

    def get_id_from_db(self, table_name, nary):
        ret = self.appdb.select_all(
            table_name,
            nary,
            self.specific_env.target.d[table_name]["id_related_columns"],
        )
        return ret

    # @abstractmethod
    def make_purchase_table_record(self, item):
        raise NotImplementedError("not implement make_purchase_table_record")

    # @abstractmethod
    def make_progress_table_record(self, item):
        raise NotImplementedError("not implement make_progress_table_record")

    def dictarray_for_purchase(self, nary):
        self.logger.debug(f"appbase.py | dictarray_for_purchase 0")
        return [self.make_purchase_table_record(item) for item in    nary]

    def dictarray_for_progress(self, nary):
        self.logger.debug(f"appbase.py | dictarray_for_progress 0")
        return [self.make_progress_table_record(item) for item in nary]

    #@abstractmethod
    def src2db_for_book(self):
        raise NotImplementedError("not implement src2db")

    #@abstractmethod
    def src2db(self):
        raise NotImplementedError("not implement src2db")

    def get_gss(
        self,
        res_path,
        table_name,
        *,
        ranges=None,
        value_render_option="FORMATTED_VALUE",
        date_time_render_option="FORMATTED_STRING",
    ):
        self.logger.debug("AppBase get_gss")
        response = {}
        gac = self.get_googleapiclientx(table_name)
        if gac:
            if ranges == None:
                range_val = "Sheet1!A1:Z"
                ranges = range_val
            self.logger.debug(
                f"ranges={ranges} value_render_option={value_render_option} date_time_render_option={date_time_render_option}"
                )
            response = gac.gss_get(
                res_path,
                ranges,
                value_render_option=value_render_option,
                date_time_render_option=date_time_render_option,
            )
            # response = {}
        return response
