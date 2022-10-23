from bookinfo.envtarget import EnvTarget
from bookinfo.envbase import EnvBase
from bookinfo.util import Util

class EnvBookstore(EnvBase):
    def __init__(self, year, db_dir):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("EnvBookstore using debug. start running")
        self.logger.debug("EnvBookstore finished running")

        kind = "bookstore"
        super().__init__(db_dir, kind)

        # fname_base = f"{kind}_{year}"
        # fname_base = f"{kind}_{year}"
        # self.logger.debug(f"EnvBookstore (fname_base_bookstore={fname_base}")
        # self.logger.debug(f"EnvBookstore (db_fname_base={fname_base}")

        spreadsheet_ids = self.vars_dict["spreadsheet_ids"]
        # self.vars_dict['db']['db_fname_base'] = fname_base
        self.vars_dict["db"]["db_year"] = year
        self.vars_dict["book"]["SPREADSHEET_ID"] = spreadsheet_ids[year]
        self.vars_dict["purchase"]["SPREADSHEET_ID"] = spreadsheet_ids[year]
        self.vars_dict["progress"]["SPREADSHEET_ID"] = spreadsheet_ids[year]
        self.set_db_name(self.target.db_dir_path)
        self.logger.debug("Calibrex finished running")

        self.logger.debug("vas_dist[db][db_file]")
        self.logger.debug(self.vars_dict["db"]["db_file"])
        self.logger.debug(f"##### EnvBookstore END { self.get_db_name() }")

    def make_db_filenamebase(self):
        filename_base = self.make_filename_base(
            "_",
            self.vars_dict["db"]["db_fname_base"],
            self.vars_dict["db"]["db_year"],
            self.vars_dict["db"]["db_id"],
        )
        return filename_base

    def get_new_db_fname_with_year(self, year):
        return super().get_new_db_fname_with_year(year)
