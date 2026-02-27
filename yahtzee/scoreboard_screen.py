"""ScoreboardScreen — modal overlay showing the top-10 leaderboard."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Static

from yahtzee.scores import get_top_10


class ScoreboardScreen(ModalScreen):
    """Leaderboard modal.  mode='postgame' or mode='peek'."""

    CSS = """
    ScoreboardScreen {
        align: center middle;
    }
    #scoreboard-dialog {
        width: 52;
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
        color: #e6edf3;
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

    def compose(self) -> ComposeResult:
        top10 = get_top_10()
        with Vertical(id="scoreboard-dialog"):
            yield Static("★  TOP SCORES  ★", id="scoreboard-title")
            if not top10:
                yield Static("No scores yet!", id="scoreboard-empty")
            else:
                lines = _build_table(top10)
                yield Static("\n".join(lines), id="scoreboard-table")
            if self._mode == "postgame":
                yield Static("Enter / N — New Game  |  Q — Quit", id="scoreboard-hint")
            else:
                yield Static("Any key — return to game", id="scoreboard-hint")

    def on_key(self, event) -> None:  # type: ignore[override]
        if self._mode == "peek":
            self.dismiss(None)

    def action_confirm_new_game(self) -> None:
        if self._mode == "postgame":
            self.dismiss("new_game")

    def action_confirm_quit(self) -> None:
        if self._mode == "postgame":
            self.dismiss("quit")


# ── helpers ──────────────────────────────────────────────────────────────────

def _build_table(entries: list[dict]) -> list[str]:
    """Return a list of strings forming an ASCII box-drawing table."""
    col_rank = 4
    col_name = 22
    col_score = 7
    col_date = 10

    sep_inner = (
        "├"
        + "─" * (col_rank + 2)
        + "┼"
        + "─" * (col_name + 2)
        + "┼"
        + "─" * (col_score + 2)
        + "┼"
        + "─" * (col_date + 2)
        + "┤"
    )
    top = (
        "┌"
        + "─" * (col_rank + 2)
        + "┬"
        + "─" * (col_name + 2)
        + "┬"
        + "─" * (col_score + 2)
        + "┬"
        + "─" * (col_date + 2)
        + "┐"
    )
    bottom = (
        "└"
        + "─" * (col_rank + 2)
        + "┴"
        + "─" * (col_name + 2)
        + "┴"
        + "─" * (col_score + 2)
        + "┴"
        + "─" * (col_date + 2)
        + "┘"
    )

    def row(rank: str, name: str, score: str, dt: str) -> str:
        return (
            f"│ {rank:<{col_rank}} │ {name:<{col_name}} │ {score:>{col_score}} │ {dt:<{col_date}} │"
        )

    lines: list[str] = [
        top,
        row("Rank", "Name", "Score", "Date"),
        sep_inner,
    ]
    for i, entry in enumerate(entries, start=1):
        lines.append(
            row(
                str(i),
                str(entry.get("name", ""))[:col_name],
                str(entry.get("score", "")),
                str(entry.get("date", "")),
            )
        )
    lines.append(bottom)
    return lines
