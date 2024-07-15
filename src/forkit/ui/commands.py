from typing import Final, Type

from textual.command import DiscoveryHit, Provider, Hit, Hits
from textual.types import IgnoreReturnCallbackType


class Cmd:
    def __init__(
        self,
        display: str,
        action: IgnoreReturnCallbackType,
        help: str = "",
        raw: str | None = None,
    ) -> None:
        self.display = display
        self.raw = display[2:].lower() if raw is None else raw
        self.help = help
        self.action = action
        self.show: bool = True


class BaseCommandProvider(Provider):

    commands: dict[str, Cmd]

    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query.lower())
        for command in self.commands.values():
            score = matcher.match(command.raw)
            if score and command.show:
                yield Hit(
                    score,
                    matcher.highlight(command.display),
                    command.action,
                    command.raw,
                    command.help,
                )

    async def discover(self) -> Hits:
        for command in self.commands.values():
            if command.show:
                yield DiscoveryHit(
                    command.display, command.action, command.raw, command.help
                )


class AppCmds(BaseCommandProvider):

    @staticmethod
    def settings() -> None:
        raise NotImplementedError

    commands = {
        "settings": Cmd(
            "⚙ Open Settings",
            help="Open the settings panel (alternatively edit settings at {Config.file})",
            action=settings,
        )
    }


class DashCmds(BaseCommandProvider):

    @staticmethod
    def open_repo() -> None:
        raise NotImplementedError

    @staticmethod
    def clone_repo() -> None:
        raise NotImplementedError

    @staticmethod
    def create_repo() -> None:
        raise NotImplementedError

    commands = {
        "open": Cmd("📁   Open a local repository", open_repo),
        "clone": Cmd("  Clone a remote repository", clone_repo),
        "new": Cmd("＋   Create a new repository", create_repo),
    }


providers: Final[dict[str, Type[BaseCommandProvider]]] = {
    cls.__name__[:-4]: cls for cls in BaseCommandProvider.__subclasses__()
}
