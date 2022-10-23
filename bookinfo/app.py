import sys

from bookinfo.cli import Cli
from bookinfo.kindlexml import KindleXML
from bookinfo.kindlejson import KindleJSON
from bookinfo.calibrex import Calibrex
from bookinfo.bookstore import Bookstore

from bookinfo.util import Util
from logging import (
    CRITICAL,
    ERROR,
    WARNING,
    INFO,
    DEBUG,
    NOTSET,
)

class App:
    @classmethod
    def __init__(self, configx):
        #
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("main using debug. start running")
        self.logger.debug("main finished running")
        #
        # Util.basicConfig(level=CRITICAL)
        # Util.basicConfig(level=ERROR)
        # Util.basicConfig(level=WARNING)
        # Util.basicConfig(level=INFO)
        # Util.basicConfig(level=DEBUG)  # デバッグ時にアンコメント
        # Util.basicConfig(level=NOTSET)
        # Util.basicConfig(filename="bookinfo.log", encoding="utf-8", level=DEBUG)
        Util.basicConfigx("bookinfo.log", "utf-8", DEBUG)
        # Util.basicConfig(filename="bookinfo.log", encoding="utf-8", level=CRITICAL)
        #
        self.configx = configx
        self.cli = Cli()

    def db_process(self, target_name, cmd, year=None):
        self.logger.info("target_name=%s cmd=%s year=%s" % (target_name, cmd, year))
        self.logger.debug("============= 0")
        if cmd == "createall":
            if target_name == "bookstore":
                for y in range(2014, 2023):
                    year = f"{y}"
                    specific_env, inst = self.cli.get_inst(
                        self.configx, target_name, cmd, year
                    )
                    self.logger.debug(f"db_process inst={inst}")
                    self.logger.debug(
                        f"db_process target_name={target_name}"
                    )
                    self.logger.debug(
                        f"db_process specific_env={specific_env}"
                    )
                    self.cli.cmd_create(inst, self.configx)
                    self.logger.debug(f"============= 0 year={year}")
            else:
                self.logger.debug("============= 0 1")
                pass

            self.logger.debug("============= 0 2")
            return None
        elif cmd == "updateall":
            if target_name == "bookstore":
                for y in range(2014, 2023):
                    specific_env, inst = self.cli.get_inst(
                        self.configx, target_name, cmd, y
                    )
                    inst.cmd_update(target_name, y)

            else:
                self.logger.debug("============= 0 3")
                pass
            self.logger.debug("============= 0 4")
            return None


        self.logger.debug("============= 1 x")
        specific_env, inst = self.cli.get_inst(self.configx, target_name, cmd, year)
        self.logger.debug("============= 1 y")

        self.logger.debug("============= 1")
        if specific_env == None:
            return None

        self.logger.debug("============= 2")

        if cmd == "create":
            self.logger.info("call cmd_create")
            self.cli.cmd_create(inst, self.configx)
        elif cmd == "update":
            if target_name == "bookstore":
                inst.cmd_update(target_name, year)
            else:
                inst.cmd_update(target_name)
        elif cmd == "append":
            self.cli.cmd_append(inst, target_name, specific_env)
        else:
            self.logger.error(f"unknown command: {cmd}")
            sys.exit(1)
        inst.db_close()
