"""QuitConfirmScreen — confirmation dialog when Q or Ctrl+C is pressed."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Static


class QuitOption(Static, can_focus=True):
    """A selectable option in the quit dialog."""

    BINDINGS = [
        ("enter", "select", ""),
        ("up", "focus_prev_option", ""),
        ("down", "focus_next_option", ""),
        ("escape", "cancel", ""),
    ]

    def __init__(self, label: str, value: bool, *, id: str) -> None:
        super().__init__(label, id=id)
        self._value = value

    def action_select(self) -> None:
        self.screen.dismiss(self._value)

    def action_cancel(self) -> None:
        self.screen.dismiss(False)

    def action_focus_prev_option(self) -> None:
        self.screen.focus_previous()

    def action_focus_next_option(self) -> None:
        self.screen.focus_next()


class QuitConfirmScreen(ModalScreen):
    """Confirmation dialog shown when Q or Ctrl+C is pressed."""

    CSS = """
    QuitConfirmScreen {
        align: center middle;
    }
    #quit-dialog {
        width: 40;
        height: auto;
        border: double #ff7b72;
        background: #16213e;
        padding: 1 2;
    }
    #quit-title {
        text-align: center;
        color: #ff7b72;
        text-style: bold;
        padding-bottom: 1;
    }
    QuitOption {
        text-align: center;
        padding: 0 1;
        color: #e6edf3;
    }
    QuitOption:focus {
        background: #2d333b;
        color: #58a6ff;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="quit-dialog"):
            yield Static("Quit Yahtzee?", id="quit-title")
            yield QuitOption("Yes — quit", True, id="opt-yes")
            yield QuitOption("No — keep playing", False, id="opt-no")

    def on_mount(self) -> None:
        self.query_one("#opt-no", QuitOption).focus()
