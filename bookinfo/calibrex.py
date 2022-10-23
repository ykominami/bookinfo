# from logging import basicConfig, getLogger, DEBUG
import xml.etree.ElementTree as ET
import os
import csv

from bookinfo.appbase import AppBase
from bookinfo.appdb import AppDb
from bookinfo.util import Util


class Calibrex(AppBase):
    def __init__(self, env, env_gcp, cmd):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("Calibrex using debug. start running")
        self.logger.debug("Calibrex finished running")

        super().__init__(env, env_gcp, cmd)

    def make_purchase_table_record(self, id_xxid):
        # TOD: 初期実装の改善。現在は外部テーブル参照のみ設定
        ret_dict = {
            "xxid": id_xxid[1],
            "ext_id": id_xxid[0],
            "purchase_date": None,
            "year": None,
            "month": None,
            "day": None,
            "year_month": None,
            "year_month_day": None,
        }

        return ret_dict

    def csv2dictarray(self, incsvfile, new_id_field, id_fields):
        ret = False
        array = []
        with open(incsvfile, encoding=self.encoding, newline=self.newline) as f:
            r = csv.DictReader(f)
            for dictx in r:
                key_id_value = "-".join([dictx[k] for k in id_fields])
                dictx[new_id_field] = key_id_value
                array.append(dictx)
        return array

    def dictarray_for_purchase(self, id_xxid_list):
        self.logger.debug(f"calibrex.py | dictarray_for_purchase 0")
        return [self.make_purchase_table_record(id_xxid) for id_xxid in id_xxid_list]

    def make_progress_table_record(self, id_xxid):
        # TOD: 初期実装の改善。現在は外部テーブル参照のみ設定
        ret_dict = {
            "xxid": id_xxid[1],
            "ext_id": id_xxid[0],
            "progress_date": None,
            "year": None,
            "month": None,
            "day": None,
            "year_month": None,
            "year_month_day": None,
        }

        return ret_dict

    def dictarray_for_progress(self, id_xxid_list):
        self.logger.debug(f"calibrex.py | dictarray_for_progress 0")
        return [self.make_purchase_table_record(id_xxid) for id_xxid in id_xxid_list]

    def src2db_for_book(self, nary):
        table_name = 'book'
        self.logger.debug(f"src2db {table_name}")
        csv_dict = self.specific_env.target.d["csv"]
        incsvfile = csv_dict["incsvfile"]
        new_id_field = csv_dict["new_id_field"]
        id_fields = csv_dict["id_fields"]

        nary2 = nary + self.csv2dictarray(incsvfile, new_id_field, id_fields)
        self.logger.debug(f"src2db nary2 len={len(nary2)}")
        ret = self.dictarray2db(table_name, nary2, new_id_field)
        return ret

    def cmd_update(self, target_name):
        self.logger.debug(f"update table {target_name}")
        db_fname = self.specific_env.get_latest_db_fname()
        self.logger.debug(db_fname)
        self.logger.debug("------")
        self.specific_env.set_db_file(db_fname)

        self.dict_filename = { name: self.make_pickle_filename(target_name, name) for name in self.names }

        nary = []
        table_name = "book"
        ret = self.src2db_for_book(nary)
        fname = f"{target_name}.pickle"
        res_path = os.path.join("pickles", target_name, fname)

        value_input_option = "USER_ENTERED"
        self.db2gss_update(res_path, "book", value_input_option, clear_flag=True)

        self.update_table_purchase_and_progress(res_path, value_input_option)
