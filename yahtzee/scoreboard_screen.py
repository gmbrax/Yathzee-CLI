"""ScoreboardScreen — modal overlay showing the top-10 leaderboard."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import DataTable, Static

from yahtzee.scores import get_top_10


class ScoreboardScreen(ModalScreen):
    """Leaderboard modal.  mode='postgame' or mode='peek'."""

    CSS = """
    ScoreboardScreen {
        align: center middle;
    }
    #scoreboard-dialog {
        width: 60;
        height: auto;
        border: double #f0883e;
        background: #16213e;
        padding: 1 2;
    }
    #scoreboard-title {
        text-align: center;
        color: #f0883e;
        text-style: bold;
        padding-bottom: 1;
    }
    #scoreboard-table {
        height: auto;
        background: #16213e;
    }
    #scoreboard-empty {
        text-align: center;
        color: #8b949e;
        padding: 1 0;
    }
    #scoreboard-hint {
        text-align: center;
        color: #8b949e;
        padding-top: 1;
    }
    """

    BINDINGS = [
        ("enter", "confirm_new_game", "New Game"),
        ("n", "confirm_new_game", "New Game"),
        ("q", "confirm_quit", "Quit"),
    ]

    def __init__(self, mode: str = "peek") -> None:
        super().__init__()
        self._mode = mode
        self._top10 = get_top_10()

    def compose(self) -> ComposeResult:
        with Vertical(id="scoreboard-dialog"):
            yield Static("★  TOP SCORES  ★", id="scoreboard-title")
            if not self._top10:
                yield Static("No scores yet!", id="scoreboard-empty")
            else:
                yield DataTable(id="scoreboard-table", cursor_type="none")
            if self._mode == "postgame":
                yield Static("Enter / N — New Game  |  Q — Quit", id="scoreboard-hint")
            else:
                yield Static("Any key — return to game", id="scoreboard-hint")

    def on_mount(self) -> None:
        if not self._top10:
            return
        table = self.query_one(DataTable)
        table.add_columns("Rank", "Name", "Score", "Date")
        for i, entry in enumerate(self._top10, start=1):
            table.add_row(
                str(i),
                str(entry.get("name", "")),
                str(entry.get("score", "")),
                str(entry.get("date", "")),
            )

    def on_key(self, event) -> None:  # type: ignore[override]
        if self._mode == "peek":
            self.dismiss(None)

    def action_confirm_new_game(self) -> None:
        if self._mode == "postgame":
            self.dismiss("new_game")

    def action_confirm_quit(self) -> None:
        if self._mode == "postgame":
            self.dismiss("quit")
