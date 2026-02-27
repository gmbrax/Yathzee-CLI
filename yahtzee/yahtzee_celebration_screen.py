"""YahtzeeCelebrationScreen — modal overlay shown when a Yahtzee is rolled."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Static

YAHTZEE_ART = """\
Y   Y  AAAAA  H   H  TTTTT  ZZZZZ  EEEEE  EEEEE  !
 Y Y   A   A  H   H    T      Z    E      E      !
  Y    AAAAA  HHHHH    T     Z     EEEE   EEEE   !
  Y    A   A  H   H    T    Z      E      E
  Y    A   A  H   H    T    ZZZZZ  EEEEE  EEEEE  !\
"""


class YahtzeeCelebrationScreen(ModalScreen):
    """Celebration overlay shown when the player rolls a Yahtzee."""

    CSS = """
    YahtzeeCelebrationScreen {
        align: center middle;
    }
    #celebration-dialog {
        width: 62;
        height: auto;
        border: double #f7c948;
        background: #16213e;
        padding: 2 4;
    }
    #celebration-art {
        text-align: center;
        color: #f7c948;
        text-style: bold;
        padding-bottom: 1;
    }
    #celebration-hint {
        text-align: center;
        color: #8b949e;
    }
    """

    BINDINGS = [
        ("enter", "continue_game", "Continue"),
        ("space", "continue_game", "Continue"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="celebration-dialog"):
            yield Static(YAHTZEE_ART, id="celebration-art")
            yield Static("Press Enter or Space to continue", id="celebration-hint")

    def action_continue_game(self) -> None:
        self.dismiss()
