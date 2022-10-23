from logging import basicConfig, getLogger, DEBUG
import json
import os
from turtle import end_fill
from pathlib import Path
import pickle
import sys

from logging import (
    basicConfig,
    getLogger,
    CRITICAL,
    ERROR,
    WARNING,
    INFO,
    DEBUG,
    NOTSET,
)


class Util:
    logger = None

    @classmethod
    def getLoggerx(cls, name):
        return getLogger(name)

    @classmethod
    def basicConfigx(cls, filename, encoding, level):
        basicConfig(filename=filename, encoding=encoding, level=level)

    @classmethod
    def escape_single_quote_in_str(cls, s):
        return s.replace("'", "''")

    @classmethod
    def escape_single_quote_in_list(cls, s):
        return [cls.escape_single_quote(i) for i in s]

    @classmethod
    def escape_single_quote_in_dict(cls, s):
        return { key : cls.escape_single_quote(s[key]) for key in s.keys() }

    @classmethod
    def escape_single_quote(cls, s):
        x = type(s)
        if x == str:
            return cls.escape_single_quote_in_str(s)
        elif x == list:
            return cls.escape_single_quote_in_list(s)
        elif x == dict:
            return cls.escape_single_quote_in_dict(s)
        else:
            return s

    @classmethod
    def escape_single_quote_all(cls, nary, text_fields, array_to_string_fields=[]):
        for dict in nary:
            for f_text in text_fields:
                if dict.get(f_text, None) != None:
                    dict[f_text] = cls.escape_single_quote(dict[f_text])
            for f_array in array_to_string_fields:
                dict[f_array] = "".join(  cls.escape_single_quote(dict[f_array])  )

    @classmethod
    def save_as_file(cls, content, fname):
        with open(fname, mode="w", encoding="utf-8") as f:
            f.write(content)

    @classmethod
    def load_file(cls, fname):
        content = None
        with open(fname, mode="r", encoding="utf-8") as f:
            content = f.read(content)
        return content

    @classmethod
    def json2str(cls, response):
        content = json.dumps(response, separators=(",", ":"), sort_keys=True, indent=4)
        return content

    @classmethod
    def json2file(cls, response, fname):
        content = cls.json2str(response)
        Util.save_as_file(content, fname)

    @classmethod
    def file2json(cls, fname):
        content = Util.load_file(fname)
        dec = json.loads(content)
        return dec

    @classmethod
    def load_pickle(cls, res_path):
        response = None
        if cls.logger == None:
            cls.logger = Util.getLoggerx(__name__)

        if os.path.exists(res_path):
            try:
                with open(res_path, "rb") as resx:
                    response = pickle.load(resx)
            except Exception as err:
                cls.logger.critical(err)
                cls.logger.critical(f"Exception: {sys.exc_info()[0]}")

            if response:
                cls.logger.critical("load_pckle 10 pickle.load")
                cls.logger.critical(
                    f"load_pickle {response}"
                )
        return response

    @classmethod
    def save_pickle(cls, res_path, value):
        ret = False
        if cls.logger == None:
            cls.logger = Util.getLoggerx(__name__)

        if not os.path.exists(res_path):
            path = Path(res_path)
            parent_path = path.parent
            os.makedirs(parent_path, exist_ok=True)

        try:
            with open(res_path, "wb") as resx:
                pickle.dump(value, resx)
                ret = True
        except Exception as err:
            cls.logger.critical(err)
            cls.logger.critical(f"Exception: {sys.exc_info()[0]}")

        return ret

    @classmethod
    def factory(cls, data):
        frame = sys._getframe().f_back
        data['filename'] = frame.f_code.co_filename
        data['lineno'] = frame.f_lineno
        return (data)
