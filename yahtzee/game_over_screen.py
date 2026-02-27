"""GameOverScreen — modal overlay shown when all 13 categories are committed."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Static


class GameOverScreen(ModalScreen):
    """End-of-game overlay showing final score and prompting for a new game."""

    CSS = """
    GameOverScreen {
        align: center middle;
    }
    #game-over-dialog {
        width: 40;
        height: auto;
        border: double #58a6ff;
        background: #16213e;
        padding: 1 2;
    }
    #game-over-title {
        text-align: center;
        color: #58a6ff;
        text-style: bold;
        padding-bottom: 1;
    }
    #game-over-bonus {
        text-align: center;
        padding-bottom: 1;
    }
    #game-over-score {
        text-align: center;
        color: #e6edf3;
        text-style: bold;
        padding-bottom: 1;
    }
    #game-over-hint {
        text-align: center;
        color: #8b949e;
    }
    """

    BINDINGS = [("n", "new_game", "New Game")]

    def __init__(self, grand_total: int, bonus_earned: bool) -> None:
        super().__init__()
        self._grand_total = grand_total
        self._bonus_earned = bonus_earned

    def compose(self) -> ComposeResult:
        with Vertical(id="game-over-dialog"):
            yield Static("★  GAME OVER  ★", id="game-over-title")
            if self._bonus_earned:
                yield Static("+35 BONUS earned!", id="game-over-bonus", classes="bonus-earned")
            else:
                yield Static("Bonus not earned", id="game-over-bonus", classes="bonus-missed")
            yield Static(f"Final Score:  {self._grand_total}", id="game-over-score")
            yield Static("Press N to play again", id="game-over-hint")

    def action_new_game(self) -> None:
        self.dismiss(True)
