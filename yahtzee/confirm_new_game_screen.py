"""ConfirmNewGameScreen — confirmation dialog when N is pressed mid-game."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.events import Key
from textual.screen import ModalScreen
from textual.widgets import Static


class ConfirmNewGameScreen(ModalScreen):
    """Confirmation dialog shown when N is pressed while a game is in progress."""

    CSS = """
    ConfirmNewGameScreen {
        align: center middle;
    }
    #confirm-dialog {
        width: 46;
        height: auto;
        border: double #f0883e;
        background: #16213e;
        padding: 1 2;
    }
    #confirm-title {
        text-align: center;
        color: #f0883e;
        text-style: bold;
        padding-bottom: 1;
    }
    #confirm-hint {
        text-align: center;
        color: #8b949e;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="confirm-dialog"):
            yield Static("Start a new game?", id="confirm-title")
            yield Static("(Y to confirm, any other key to cancel)", id="confirm-hint")

    def on_key(self, event: Key) -> None:
        if event.key == "y":
            self.dismiss(True)
        else:
            self.dismiss(False)
