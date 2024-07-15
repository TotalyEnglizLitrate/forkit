# TODO: add a Characters class for switching between ascii and nerfont ligatures


from __future__ import annotations

from pathlib import Path
from typing import Literal

from platformdirs import user_cache_path, user_config_path
from rich import print

import forkit.app

_exit = exit


def exit(msg: str):
    app = forkit.app.ctx.app
    if app.is_running:
        app.exit()
    print(msg)
    _exit(1)


class CustomPath(Path):

    def __init__(
        self,
        *args,
        err_msg: str,
        err_level: Literal[50] | Literal[40] | Literal[30] | Literal[20],
        fallback: CustomPath | None = None,
    ) -> None:
        super().__init__(*args)
        if not self.exists():
            err_msg = err_msg.replace("#path", self.__str__())
            forkit.app.logger.log(err_level, err_msg)
            if err_level == 50:
                exit(f"[bold red]CRITICAL ERROR[/]: {err_msg}")
            elif fallback is not None:
                self = fallback


class DefaultPaths:
    conf_dir = user_config_path("Forkit")
    cache_dir = user_cache_path("Forkit")
    conf_file = CustomPath(
        conf_dir / "Config.toml",
        err_msg="No custom configuration found, using default configuration",
        err_level=20,
    )
    theme_file = CustomPath(
        conf_dir / "Theme.toml",
        err_msg="No custom theme found, using default theme",
        err_level=20,
    )
    cred_file = CustomPath(
        cache_dir / "Credentials.json",
        err_msg="No credentials found, any remote functionality requiring authentication will not work",
        err_level=30,
    )
    opened_repos = CustomPath(
        cache_dir / "history.json",
        err_msg="Repository history not found, no repositories have been opened yet",
        err_level=20,
    )
    resource_files = CustomPath(
        Path(__file__).parents[2] / "res",
        err_msg="App resource folder at #path not found, reinstall forkit to fix",
        err_level=50,
    )
    default_conf = CustomPath(
        resource_files / "Config.toml",
        err_msg="Default config file at #path not found",
        err_level=50,
    )
    default_theme = CustomPath(
        resource_files / "Theme.toml",
        err_msg="Default theme file at #path not found",
        err_level=50,
    )
    log_dir = cache_dir / "logs"


class RuntimePaths(DefaultPaths): ...
