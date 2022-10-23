# from logging import basicConfig, getLogger, DEBUG
import json
import os
from bookinfo.appbase import AppBase
from bookinfo.util import Util

import pprint

class Bookstore(AppBase):
    def __init__(self, specific_env, env_gcp, cmd):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("Bookstore using debug. start running")
        self.logger.debug("Bookstore finished running")

        self.pp = pprint.PrettyPrinter(indent=4)

        super().__init__(specific_env, env_gcp, cmd)

    def load_jsonfile(self, jsonfname):
        with open(jsonfname) as f:
            parsed = json.load(f)
            self.register_data(parsed)

    def make_json_filename(self, basename, year):
        return f"{basename}-{year}.json"

    def make_pickle_filename_for_target_name(self, target_name, year_str, name):
        fname = self.make_pickle_filename(target_name, self.pickle_ext_name)
        res_path = os.path.join(self.pickle_dir_name, target_name, year_str, name, fname)
        return res_path

    def cmd_update(self, target_name, year):
        self.logger.debug(f"bookstore.py Bookstore update table {target_name}")

        self.dict_filename = { name: self.make_pickle_filename_for_target_name(target_name, str(year), name) for name in self.names }

        name = self.BOOK
        ranges = self.specific_env.target.d[name]["RANGE_NAME"]

        response = self.get_gss(self.dict_filename[name], name, ranges=ranges)

        book_fname = self.make_json_filename(name, year)

        Util.json2file(response, book_fname)
        self.load_jsonfile(book_fname)

        value_input_option = "USER_ENTERED"

        self.update_table_purchase_and_progress(value_input_option)

    def make_purchase_table_record(self, item):
        ret_dict = {
            "xxid": None,
            "ext_id": item[0],
            "purchase_date": item[1],
            "year": None,
            "month": None,
            "day": None,
            "year_month": None,
            "year_month_day": None,
        }

        return ret_dict

    def make_progress_table_record(self, item):
        # TOD: 初期実装の改善。現在は外部テーブル参照のみ設定
        ret_dict = {
            "xxid": None,
            "ext_id": item[0],
            "progress_date": None,
            "year": None,
            "month": None,
            "day": None,
            "year_month": None,
            "year_month_day": None,
        }

        return ret_dict

    # def make_progress_table_record(self, item):
    #    raise NotImplementedError("not implement make_progress_table_record")
