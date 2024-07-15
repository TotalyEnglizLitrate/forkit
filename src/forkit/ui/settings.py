from textual.app import ComposeResult
from textual.screen import Screen


class Settings(Screen):
    def compose(self) -> ComposeResult:
        raise NotImplementedError
