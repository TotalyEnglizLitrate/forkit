from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer

from forkit.config.conf import Config
from forkit.ui.dash import Dashboard
from forkit.ui.commands import AppCmds
from forkit.ui.settings import Settings
from forkit.ui.help import Help


class Forkit(App[None]):
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

    CONF: Config = Config()

    def compose(self) -> ComposeResult:
        self.switch_mode("main")
        yield Footer()


def main():
    Forkit().run()
