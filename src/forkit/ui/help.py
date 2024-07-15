from textual.app import ComposeResult
from textual.screen import Screen


class Help(Screen):
    def compose(self) -> ComposeResult:
        raise NotImplementedError
