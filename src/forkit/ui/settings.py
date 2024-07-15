from textual.app import ComposeResult
from textual.screen import Screen

# TODO: 3 tabs - config, theme, git Settings
# TODO: Create set of base settings widgets (bool, options, int, float, ....)


class Settings(Screen):
    def compose(self) -> ComposeResult:
        raise NotImplementedError
