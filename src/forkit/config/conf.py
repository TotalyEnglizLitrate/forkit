from argparse import Namespace
from copy import deepcopy
from typing import Any

from toml import dump, load, loads

from forkit.misc import CustomPath, DefaultPaths, RuntimePaths
from forkit.app import logger


class ConfigurationError(Exception):
    pass


class Config:
    def __init__(self, args: Namespace) -> None:
        self.file: CustomPath = args.config
        self.default: dict = load(DefaultPaths.resource_files / "Config.toml")
        self.file_only: dict = load(self.file)
        self.with_defaults: dict = self.fill_defaults(deepcopy(self.file_only))
        # TODO: fill in the string
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

        iter_check = (k for k in conf_dict if k not in default_dict)
        for k in iter_check:
            logger.log(40, f"Unkown key {key + k} in configuration")
            conf_dict.pop(k)

        for k, v in default_dict:
            if k not in conf_dict:
                conf_dict[k] = v
            elif self.is_valid(k, v):
                if isinstance(v, dict):
                    self.fill_defaults(conf_dict[k], default_dict[k], key + k)
            else:
                logger.log(
                    40, "Invalid key: value pair, expected #mapping_get_type_here"
                )
                conf_dict[k] = v

        return conf_dict

    def is_valid(self, key: str, value: str) -> bool:
        # TODO: Create a key: value type mapping and verify it here
        raise NotImplementedError

    def get_type(self, key: str) -> Any:
        # todo: Key value mapper? or a dict? idk
        raise NotImplementedError
