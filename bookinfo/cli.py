import pprint
from bookinfo.util import Util

class Cli:
    def __init__(self):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("Cli using debug. start running")
        self.logger.debug("Cli finished running")
        self.pp = pprint.PrettyPrinter(indent=4)

    def cmd_append(self, inst, target_name, target):
        nary = []
        inst.db2gss_append("purchase")

    def cmd_create(self, inst, configx):
        self.logger.info("cmd_create")
        inst.create_tables(configx)

    def get_inst(self, configx, target_name, cmd, year=None):
        self.logger.debug(f"get_inst 0 cmd={cmd}")
        if not target_name in configx.d["klass"]:
            self.logger.critical(f"{target_name} is not in configx.d")
            self.logger.critical(configx.d["klass"])
            return [None, None]
        if target_name == "bookstore":
            self.logger.debug(
                f"get_inst 1 y configx.d[target_name].keys()={configx.d[target_name].keys()}"
            )
            specific_env = configx.d[target_name][str(year)]
            if cmd == "create":
                db_fname = specific_env.get_new_db_fname_with_year(year)
                self.logger.debug(db_fname)
                self.logger.debug(f"get_inst create db_fname={db_fname}")
                specific_env.set_db_file(db_fname)
            elif cmd == "update":
                db_fname = specific_env.get_latest_db_fname_with_year(year)
                self.logger.debug(f"get_inst update db_fname={db_fname}")
                specific_env.set_db_file(db_fname)

        else:
            self.logger.debug("configx.d.keys()")
            self.logger.debug(configx.d.keys())
            self.logger.debug("configx.d.keys ====")
            specific_env = configx.d[target_name]
            if cmd == "create":
                db_fname = specific_env.get_new_db_fname()
                self.logger.debug(f"get_inst create db_fname={db_fname}")
                specific_env.set_db_file(db_fname)
            elif cmd == "update":
                db_fname = specific_env.get_latest_db_fname()
                self.logger.debug(f"get_inst update db_fname={db_fname}")
                specific_env.set_db_file(db_fname)

        self.logger.debug("get_inst 1 x specific_env={}".format(specific_env))
        if specific_env == None:
            self.logger.critical("{target_name} is None")
            self.logger.critical("{configx.d[target_name]} is None")
            self.logger.critical("year={year}")
            return [None, None]

        klass = configx.d["klass"][target_name]
        gcp = configx.d["gcp"]
        inst = klass(specific_env, gcp, cmd)

        self.logger.debug("get_inst 3 = [specific_env, inst]")
        return [specific_env, inst]

    def not_white_space(self, s):
        if s == "":
            return False
        else:
            return True

    def len_11(self, s):
        if len(s) > 11:
            return True
        else:
            return False

    def to_integer(self, val):
        return int(val)

    def to_string(self, val):
        return str(val)

    def convert_for_table(self, key, value):
        dictx = {
            "totalID": self.to_integer,
            "xid": self.to_integer,
            "purchase_date": self.to_string,
            "bookstore": self.to_string,
            "title": self.to_string,
            "ASIN": self.to_string,
            "read_status": self.to_integer,
            "shape": self.to_integer,
            "category": self.to_string,
        }
        return dictx[key](value)

    def reform_row(self, row):
        return list(filter(self.not_white_space, row))

    def cmd_jsonx(self, year=None):
        if year == None:
            fname = "book.json"
        else:
            fname = f"book-{year}.json"

        with open(fname, mode="r", encoding="utf-8") as f:
            content = f.read()
        response = json.loads(content)
        len_11_obj = filter(len_11, response["values"][1:])
        map_obj = map(self.reform_row, len_11_obj)
        headers = self.reform_row(response["values"][0])
        xlistx = [
            {z[0]: self.convert_for_table(z[0], z[1]) for z in zip(headers, row)}
            for row in map_obj
        ]
        for l in xlistx:
            self.logger.debug(l)

    def cmd_create_table(self, inst, title):
        inst.create_table("book", title)
