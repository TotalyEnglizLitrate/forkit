from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

from forkit.misc import CustomPath, DefaultPaths


parser = ArgumentParser("forkit")
parser.add_argument(
    "c",
    "config",
    type=lambda x: CustomPath(
        x,
        err_msg="Custom config file not found at #path, using default configuration",
        err_level=40,
        fallback=DefaultPaths.default_conf,
    ),
    required=False,
    default=DefaultPaths.conf_file,
)
parser.add_argument(
    "t",
    "theme",
    type=lambda x: CustomPath(
        x,
        err_msg="Custom theme file not found at #path, using default theme",
        err_level=40,
        fallback=DefaultPaths.default_conf,
    ),
    required=False,
    default=DefaultPaths.theme_file,
)
parser.add_argument(
    "log-level", choices={"debug", "warn", "err"}, required=False, default="warn"
)
parser.add_argument(
    "log-file",
    type=Path,
    required=False,
    default=DefaultPaths.log_dir / f"{datetime.now().strftime('%d%m%Y_$H$M$S.log')}",
)
