from bookinfo.envtarget import EnvTarget
from bookinfo.envbase import EnvBase
from bookinfo.util import Util

class EnvKindle(EnvBase):
    def __init__(self, db_dir, kind = None):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("EnvKindle using debug. start running")
        self.logger.debug("EnvKindle finished running")

        if kind == None:
          kind = "kindle"

        super().__init__(db_dir, kind)

        book = self.vars_dict["book"]
        book["table_columns"] = self.vars_dict["table_columns_default"]
        self.set_db_name(self.target.db_dir_path)
