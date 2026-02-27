"""NameEntryScreen — modal overlay for entering a player name after game over."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Static


class NameEntryScreen(ModalScreen):
    """Name entry modal shown after game over so the score can be saved."""

    CSS = """
    NameEntryScreen {
        align: center middle;
    }
    #name-entry-dialog {
        width: 44;
        height: auto;
        border: double #f0883e;
        background: #16213e;
        padding: 1 2;
    }
    #name-entry-title {
        text-align: center;
        color: #f0883e;
        text-style: bold;
        padding-bottom: 1;
    }
    #name-entry-hint {
        text-align: center;
        color: #8b949e;
        padding-top: 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="name-entry-dialog"):
            yield Static("Game Over — Enter your name", id="name-entry-title")
            yield Input(placeholder="Anonymous", max_length=20, id="name-input")
            yield Static("Enter — save score", id="name-entry-hint")

    def on_mount(self) -> None:
        self.query_one("#name-input", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        name = event.value.strip() or "Anonymous"
        self.dismiss(name)
