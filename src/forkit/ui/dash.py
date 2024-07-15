from __future__ import annotations
from typing import Type

from textual.app import ComposeResult, on
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Static

from .commands import BaseCommandProvider, DashCmds, providers


class Dashboard(Screen):

    BINDINGS = [Binding("O o", show=False, action="run('open')")]

    AUTO_FOCUS = None

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static(
                """
███████╗░█████╗░██████╗░██╗░░██╗██╗████████╗
██╔════╝██╔══██╗██╔══██╗██║░██╔╝██║╚══██╔══╝
█████╗░░██║░░██║██████╔╝█████═╝░██║░░░██║░░░
██╔══╝░░██║░░██║██╔══██╗██╔═██╗░██║░░░██║░░░
██║░░░░░╚█████╔╝██║░░██║██║░╚██╗██║░░░██║░░░
╚═╝░░░░░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░╚═╝░░░
""".strip(),
                id="logo",
            ),
            Container(
                Button(
                    "📁   Open a local repository",
                    id="button-open",
                    classes="dash-buttons",
                    variant="primary",
                ),
                Button(
                    "  Clone a remote repository",
                    id="button-clone",
                    classes="dash-buttons",
                    variant="primary",
                ),
                Button(
                    "＋   Create a new repository",
                    id="button-new",
                    classes="dash-buttons",
                    variant="primary",
                ),
                id="dash-buttons",
            ),
            id="dash",
        )

    @on(Button.Pressed)
    def handle_buttons(self, event: Button.Pressed) -> None:
        assert event.button.id is not None and "dash-buttons" in event.button.classes
        self.action_run(event.button.id[7:])

    def action_run(
        self, cmd: str, provider: Type[BaseCommandProvider] = DashCmds
    ) -> None:
        provider.commands[cmd].action()
