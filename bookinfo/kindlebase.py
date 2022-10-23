import datetime
import os
from pathlib import PurePath, Path
import re

from bookinfo.appbase import AppBase
from bookinfo.appdb import AppDb
from bookinfo.util import Util


class KindleBaseError(Exception):
    pass


class KindleBaseSubError(KindleBaseError):
    pass


class KindleBaseSub2Error(KindleBaseError):
    pass


class KindleBase(AppBase):
    def __init__(self, env, env_gcp, cmd):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("using debug. start running")
        self.logger.debug("finished running")

        super().__init__(env, env_gcp, cmd)

    def make_pickle_filename_for_target_name(self, target_name, name):
        fname = self.make_pickle_filename(target_name, self.pickle_ext_name)
        res_path = os.path.join(self.pickle_dir_name, target_name, name, fname)
        return res_path

    def make_purchase_table_record(self, item):
        ext_id = item[0]
        asin = item[1]
        purchase_date = item[2]
        if purchase_date != None:
            dt = datetime.datetime.strptime(
                purchase_date, "%Y-%m-%dT%H:%M:%S+0000"
            )
            year_str = "%04d" % dt.year
            month_str = "%02d" % dt.month
            day_str = "%02d" % dt.day
            year_month_str = "%s%s" % (year_str, month_str)
            year_month_day_str = "%s%s%s" % (year_str, month_str, day_str)
            ret_dict = {
                "asin": asin,
                "ext_id": ext_id,
                "purchase_date": purchase_date,
                "year": year_str,
                "month": month_str,
                "day": day_str,
                "year_month": year_month_str,
                "year_month_day": year_month_day_str,
            }
        else:
            ret_dict = None

        return ret_dict

    def dictarray_for_purchase(self, id_xxid_list):
        self.logger.debug(f"kindlebase.py | dictarray_for_purchase 0")
        return [self.make_purchase_table_record(id_xxid) for id_xxid in id_xxid_list]

    def make_progress_table_record(self, item):
        ext_id = item[0]
        asin = item[1]
        progress_date = None
        if progress_date != None:
            dt = datetime.datetime.strptime(
                item["progress_date"], "%Y-%m-%dT%H:%M:%S+0000"
            )
            year_str = "%04d" % dt.year
            month_str = "%02d" % dt.month
            day_str = "%02d" % dt.day
            year_month_str = "%s%s" % (year_str, month_str)
            year_month_day_str = "%s%s%s" % (year_str, month_str, day_str)
            progress_date = dt
            ret_dict = {
                "asin": asin,
                "ext_id": ext_id,
                "status": 0,
                "progress_date": progress_date,
                "year": year_str,
                "month": month_str,
                "day": day_str,
                "year_month": year_month_str,
                "year_month_day": year_month_day_str,
                "purchase_date": purchase_date
            }
        else:
            ret_dict = None

        return ret_dict

    def dictarray_for_progress(self, id_xxid_list):
        self.logger.debug(f"kindlebase.py KindleBase | dictarray_for_progress 0")
        return [self.make_progress_table_record(id_xxid) for id_xxid in id_xxid_list]

    def cmd_update(self, target_name):
        self.logger.debug(f"kindlexml.py KindleBase update table {target_name}")
        self.dict_filename = { name: self.make_pickle_filename_for_target_name(target_name, name) for name in self.names }

        name = self.BOOK
        value_input_option = "USER_ENTERED"
        db_fname = self.specific_env.get_latest_db_fname()
        self.logger.debug(db_fname)
        self.logger.debug("------")
        self.specific_env.set_db_file(db_fname)

        nary = []
        ret = self.src2db_for_book(nary)
        res_path = self.dict_filename[name]
        value_input_option = "USER_ENTERED"

        self.db2gss_update(res_path, self.BOOK, value_input_option, clear_flag=True)

        self.update_table_purchase_and_progress(value_input_option)

    def get_author_as_string(self, author):
        authors = ''

        try:
            x = type(author)
            if x == list:
                authors = ":".join([a['#text'] for a in author])
            elif x == dict:
                authors = author['#text']
            else:
                authors = authors
        except AttributeError as err:
            self.pp.pprint(err)

        return authors

    def get_record_data(self, item):
        dict = {}
        dict['asin'] = item['ASIN']
        dict['webReaderUrl'] = f"https://read.amazon.co.jp/#{item['ASIN']}"
        dict['productUrl'] = 'https://read.amazon.co.jp'
        dict['title'] = item['title']['#text']
        dict['percentageRead'] = 0
        author = item['authors']['author']
        dict['authors'] = self.get_author_as_string(author)
        dict['title'] = item['title']['#text']
        dict['resourceType'] = 'EBOOK'
        dict['originType'] = 'PURCHASE'
        dict['mangaOrComicAsin'] = 0
        dict['publication_date'] = item['publication_date']
        dict['purchase_date'] = item['purchase_date']

        return dict

    def conv_key(self, dictxarray, key_table):
        for dictx in dictxarray:
            for key, new_key in key_table.items():
                if new_key not in dictx.keys():
                    if key in dictx.keys():
                        dictx[new_key] = dictx[key]
                        del dictx[key]
                    else:
                        raise KindleXMLSubError("6")

