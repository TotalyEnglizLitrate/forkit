from pathlib import Path
from typing import NamedTuple

from platformdirs import user_cache_path, user_config_path

_conf_dir = user_config_path("Forkit")
_cache_dir = user_cache_path("Forkit")


class DefaultPaths(NamedTuple):
    conf_dir = _conf_dir
    cache_dir = _cache_dir
    conf_file = _conf_dir / "Config.toml"
    theme_file = _conf_dir / "Theme.toml"
    cred_file = _cache_dir / "Credentials.json"
    opened_repos = _cache_dir / "history.json"
    resource_files = Path(__file__).parents[2] / "res"

class RuntimePaths(DefaultPaths):
    ...
