import os
from pathlib import Path

from bookinfo.util import Util

from bookinfo.kindlexml import KindleXML
from bookinfo.kindlejson import KindleJSON
from bookinfo.calibrex import Calibrex
from bookinfo.bookstore import Bookstore

from bookinfo.envkindlexml import EnvKindleXML
from bookinfo.envkindlejson import EnvKindleJSON
from bookinfo.envcalibre import EnvCalibre
from bookinfo.envbookstore import EnvBookstore

class Configx:
    def __init__(self, kind, config):
        # ykominami@gmail.com
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("using debug. start running")
        self.logger.debug("finished running")

        self.d = {}
        self.d["klass"] = {
            "kindlexml": KindleXML,
            "kindlejson": KindleJSON,
            "calibre": Calibrex,
            "bookstore": Bookstore,
        }
        self.d["gcp"] = {}
        self.db_dir = Path(*config["db"]["db_parent_dir"])
        cred = config["credential"]
        self.d["gcp"]["credentials"] = Path(*cred["dir"], cred["file"])

        self.d["gcp"]["token"] = Path(*cred["dir"], cred["token_file"])
        self.d["gcp"]["SCOPES"] = ["https://www.googleapis.com/auth/spreadsheets"]

        if kind == "kindlexml":
            self.d[kind] = EnvKindleXML(self.db_dir)
        elif kind == "kindlejson":
            self.d[kind] = EnvKindleJSON(self.db_dir)
        elif kind == "calibre":
            self.d[kind] = EnvCalibre(self.db_dir)
        elif kind == "bookstore":
            self.d[kind] = {}
            for y in range(2014, 2023):
                year = f"{y}"
                self.d[kind][year] = EnvBookstore(year, self.db_dir)


if __name__ == "__main__":
    kind = os.argv[1]
    configx = Configx(kind)
    logger = getLogger(__name__)
    logger.debug(configx.db_dir)
