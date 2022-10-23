import sys
from pathlib import Path
import argparse
import json
from bookinfo.app import App
from bookinfo.configx import Configx

def main() -> None:
    parser = argparse.ArgumentParser(description="Process Google Spreadsheet")
    parser.add_argument(
        "target",
        help="target",
        choices=["kindlexml", "kindlejson", "calibre", "bookstore"],
    )
    parser.add_argument(
        "cmd",
        help="cmd",
        choices=[
            "create",
            "createall",
            "update",
            "updateall",
            "append",
        ],
    )
    parser.add_argument(
        "year", metavar="year", type=int, nargs="?", default=-1, help="year"
    )
    args = parser.parse_args(sys.argv[1:])
    TARGET = args.target.lower()
    CMD = args.cmd.lower()
    # YEAR = f"{args.year}"
    YEAR = int(args.year)
    if CMD == "createall" or CMD == "updateall":
        if TARGET != "bookstore":
            args2 = parser.parse_args(["-h"])
    elif TARGET == "bookstore":
        if YEAR == -1:
            args2 = parser.parse_args(["-h"])

    config_dir_path = Path("config")
    config_path = config_dir_path / "_common" / "common.json"
    config = None
    with config_path.open() as f:
        content = f.read()
        config = json.loads(content)

    configx = Configx(TARGET, config)
    app = App(configx)
    year_str = str(YEAR)
    app.db_process(TARGET, CMD, year_str)
