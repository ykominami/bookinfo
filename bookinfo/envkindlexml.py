from bookinfo.util import Util
from bookinfo.envkindle import EnvKindle

class EnvKindleXML(EnvKindle):
    def __init__(self, db_dir):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("EnvKindlexml using debug. start running")
        self.logger.debug("EnvKindlexml finished running")

        kind = "kindlexml"
        super().__init__(db_dir, kind)

        book = self.vars_dict["book"]
        book["table_columns"] = self.vars_dict["table_columns_default"]
        self.set_db_name(self.target.db_dir_path)


