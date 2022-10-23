import datetime
import json
import os
from pathlib import PurePath, Path
import re

# from bookinfo.appbase import AppBase
# from bookinfo.appdb import AppDb
from bookinfo.kindlebase import KindleBase
from bookinfo.util import Util


class KindleJSONError(Exception):
    pass


class KindleJSONSubError(KindleJSONError):
    pass


class KindleJSONSub2Error(KindleJSONError):
    pass


# class KindleJSON(AppBase):
class KindleJSON(KindleBase):
    def __init__(self, env, env_gcp, cmd):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("using debug. start running")
        self.logger.debug("finished running")

        self.json_file_list = []

        super().__init__(env, env_gcp, cmd)

    def cmd_update(self, target_name):
        self.logger.debug(f"KindleJSON update table {target_name}")
        self.dict_filename = { name: self.make_pickle_filename_for_target_name(target_name, name) for name in self.names }

        table_name = self.BOOK
        value_input_option = "USER_ENTERED"
        db_fname = self.specific_env.get_latest_db_fname()
        self.logger.debug(db_fname)
        self.logger.debug("------")
        self.specific_env.set_db_file(db_fname)

        nary = []
        name = self.BOOK
        ret = self.src2db_for_book(nary)
        res_path = self.dict_filename[name]
        book = self.specific_env.target.d[name]
        value_input_option = "USER_ENTERED"

        json_fname = self.make_json_filename(target_name)
        self.db2gss_update(res_path, self.BOOK, value_input_option, clear_flag=False)

        self.update_table_purchase_and_progress(value_input_option)

    def src2db_for_book(self, nary):
        table_name = "book"
        table_column_convert = self.specific_env.target.d["book"].get(
            "table_column_convert", []
        )
        json_dict = self.specific_env.target.d["json"]
        new_id_field = json_dict["new_id_field"]
        id_fields = json_dict["id_fields"]
        json_parent_dir = json_dict["input_json_file_parent_dir"]
        json_parent_path = Path(json_parent_dir)
        nary.extend(self.json2dictarray(json_parent_path, table_column_convert))
        ret = self.dictarray2db(table_name, nary)
        return ret

    def get_file_list_under_dir(self, listx, item):
        return listx + list(item.glob("**/*"))

    def is_numerical_named_dir(self, item):
        ret = False
        if item.is_dir() == True:
            if re.match(r"^[0-9]+$", item.name) != None:
                ret = True
        return ret

    def get_json_file_list(self, json_parent_path, pattern):
        # item_list = list(json_parent_path.glob("*.json"))
        # item_list = list(json_parent_path.glob("*/*.json"))
        # item_list = list(json_parent_path.glob("*.txt"))
        item_list = list(json_parent_path.glob(pattern))
        dir_item_list = [
            item for item in item_list if self.is_numerical_named_dir(item) == True
        ]
        sorted_dir_item_list = sorted(
            dir_item_list, reverse=True, key=lambda itemx: (itemx.name)
        )
        for item in sorted_dir_item_list:
            self.json_file_list = self.get_file_list_under_dir(
                self.json_file_list, item
            )

    def json2dictarray(self, json_parent_path, table_column_convert):
        nary = []
        xdict = {}
        self.get_json_file_list(json_parent_path, "*")
        # self.get_json_file_list(json_parent_path, "*/*.json")
        # self.get_json_file_list(json_parent_path, "*/*.txt")\
        for n in self.json_file_list:
            with Path(n).open(encoding="utf_8") as f:
                try:
                    dict = json.load(f)
                    itemlist = dict["itemsList"]
                    self.conv_key(itemlist, table_column_convert)
                    nary = nary + itemlist
                except json.decoder.JSONDecodeError as err:
                    self.logger.critical(
                        f"json2dictarray json.decoder.JSONDecodeError {err} json file={n}"
                    )

        return nary
