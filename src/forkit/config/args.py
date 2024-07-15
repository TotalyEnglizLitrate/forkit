from argparse import ArgumentParser
from pathlib import Path

from forkit.misc import DefaultPaths


parser = ArgumentParser("forkit")
parser.add_argument("c", "config", type=Path, required=False, default=DefaultPaths.conf_file)
parser.add_argument("t", "theme", type=Path, required=False, default=DefaultPaths.theme_file)
parser.add_argument(
    "l", "log-level", choices={"debug", "warn", "err"}, required=False, default="warn"
)
