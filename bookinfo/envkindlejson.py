'''
from bookinfo.envtarget import EnvTarget
from bookinfo.envbase import EnvBase
'''
from bookinfo.envkindle import EnvKindle
from bookinfo.util import Util

class EnvKindleJSON(EnvKindle):
    def __init__(self, db_dir):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("EnvKindleJSON using debug. start running")
        self.logger.debug("EnvKindleJSON finished running")

        kind = "kindlejson"
        super().__init__(db_dir, kind)
        '''
        book = self.vars_dict["book"]
        book["table_columns"] = self.vars_dict["table_columns_default"]
        self.set_db_name(self.target.db_dir_path)
        '''
