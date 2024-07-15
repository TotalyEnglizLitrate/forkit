from argparse import Namespace
from copy import deepcopy
from pathlib import Path

from toml import dump, load, loads

from forkit.misc import DefaultPaths

from .args import parser


class ConfigurationError(Exception):
    pass


class Config:
    #TODO: implement file.exists checks
    def __init__(self) -> None:
        self.args: Namespace = parser.parse_args()
        self.file: Path = self.args.config
        if not self.file.exists():
            raise NotImplementedError



        self.default: dict = load(DefaultPaths.resource_files / "Config.toml")
        self.file_only: dict = load(self.file)
        self.with_defaults: dict = self.fill_defaults(deepcopy(self.file_only))
        args_as_toml: str = (
            f"""

        """.strip()
        )
        self.args_dict: dict = loads(args_as_toml)
        self.runtime_conf: dict = self.fill_defaults(
            deepcopy(self.args_dict), self.with_defaults
        )

    def fill_defaults(
        self, conf_dict: dict, default_dict: dict | None = None, key: str | None = None
    ) -> dict:
        default_dict = default_dict or self.default
        key = f"{key}." if key is not None else ""

        iter_check = (k in default_dict for k in conf_dict)
        for k in iter_check:
            if not k:
                raise ConfigurationError(
                    f"Unkown key provided: {key}.{k} is not a valid key"
                )

        for k, v in default_dict:
            if k not in conf_dict:
                conf_dict[k] = v
            elif isinstance(v, dict):
                self.fill_defaults(conf_dict[k], default_dict[k], key + k)

        return conf_dict

    @staticmethod
    def is_valid(key: str, value: str):
        raise NotImplementedError
