import logging

from rich.logging import RichHandler
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer

from forkit.config.conf import Config
from forkit.config.args import parser
from forkit.misc import DefaultPaths, RuntimePaths
from forkit.ui.dash import Dashboard
from forkit.ui.commands import AppCmds
from forkit.ui.settings import Settings
from forkit.ui.help import Help


logger = logging.getLogger("forkit_logger")


class Forkit(App[None]):
    # TODO: see: theme.py
    CSS = """

    Dashboard {
        align: center middle;
    }
    #dash {
        height: 70%;
        width: 50%;
        padding: 2 0;
    }

    #logo {
        text-style: bold;
        color: purple;
        text-align: center;
        margin: 0 2 0 0;
    }
    #dash-buttons {
        align: center middle;
    }
    
    Button {
        content-align: center middle;
        text-align: center;
        margin: 1 0;
    }
    """

    BINDINGS = [Binding("/", action="command_palette")]

    COMMANDS = App.COMMANDS | {AppCmds}

    MODES = {"main": Dashboard, "settings": Settings, "help": Help}

    def compose(self) -> ComposeResult:
        self.switch_mode("main")
        yield Footer()


class Context:
    def __init__(self) -> None:
        self.cmd_line_args = parser.parse_args()
        logging.basicConfig(
            filename=self.cmd_line_args.log_file, handlers=[RichHandler()]
        )
        self.conf = Config(self.cmd_line_args)
        self.app = Forkit()
        self.DefaultPaths = DefaultPaths
        self.RuntimePaths = RuntimePaths


ctx = Context()
main = lambda: ctx.app.run()
