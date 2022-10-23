from bookinfo.envtarget import EnvTarget
from bookinfo.envbase import EnvBase
from bookinfo.util import Util

class EnvCalibre(EnvBase):
    def __init__(self, db_dir):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("EnvCalibre using debug. start running")
        self.logger.debug("EnvCalibrex finished running")

        kind = "calibre"
        super().__init__(db_dir, kind)

        book = self.vars_dict["book"]
        book["table_columns"] = (
            self.vars_dict["table_columns_default"]
            + self.vars_dict["csv"]["incsv_headers"]
        )
        self.set_db_name(self.target.db_dir_path)
