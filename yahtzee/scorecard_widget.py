"""ScorecardWidget — displays all 13 Yahtzee scoring categories and totals."""

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widget import Widget
from textual.widgets import Static

from game import GameState

UPPER_CATEGORIES: list[tuple[str, str]] = [
    ("ones", "Ones"),
    ("twos", "Twos"),
    ("threes", "Threes"),
    ("fours", "Fours"),
    ("fives", "Fives"),
    ("sixes", "Sixes"),
]

LOWER_CATEGORIES: list[tuple[str, str]] = [
    ("three_of_a_kind", "Three of a Kind"),
    ("four_of_a_kind", "Four of a Kind"),
    ("full_house", "Full House"),
    ("small_straight", "Small Straight"),
    ("large_straight", "Large Straight"),
    ("yahtzee", "Yahtzee"),
    ("chance", "Chance"),
]

ALL_CATEGORIES = UPPER_CATEGORIES + LOWER_CATEGORIES


class CategoryRow(Widget):
    """A single scorecard row: category name on the left, score on the right."""

    can_focus = True

    def __init__(self, key: str, label: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.key = key
        self._label = label

    def compose(self) -> ComposeResult:
        yield Static(self._label, id=f"cat-label-{self.key}", classes="row-label")
        yield Static("", id=f"cat-score-{self.key}", classes="row-score")

    def update_score(self, score: int | None) -> None:
        """Update the displayed score and apply committed styling."""
        self.query_one(f"#cat-score-{self.key}", Static).update(
            "" if score is None else str(score)
        )
        if score is not None:
            self.add_class("committed")
        else:
            self.remove_class("committed")


class ScorecardWidget(VerticalScroll):
    """Full Yahtzee scorecard: upper + lower sections, subtotal, bonus, and grand total."""

    can_focus = False

    def compose(self) -> ComposeResult:
        yield Static("── UPPER SECTION ──", classes="section-header")
        for key, label in UPPER_CATEGORIES:
            yield CategoryRow(key, label, id=f"row-{key}")
        yield Static("", id="subtotal-row", classes="totals-row")
        yield Static("", id="bonus-row", classes="totals-row")
        yield Static("", id="bonus-hint-row", classes="bonus-hint")
        yield Static("── LOWER SECTION ──", classes="section-header")
        for key, label in LOWER_CATEGORIES:
            yield CategoryRow(key, label, id=f"row-{key}")
        yield Static("", id="total-row", classes="totals-row grand-total")

    def refresh_scores(self, game: GameState) -> None:
        """Sync all displayed values with the current GameState."""
        for key, _ in ALL_CATEGORIES:
            self.query_one(f"#row-{key}", CategoryRow).update_score(game.scores[key])

        subtotal = game.upper_subtotal
        self.query_one("#subtotal-row", Static).update(f"Subtotal: {subtotal} / 63")

        if game.bonus > 0:
            self.query_one("#bonus-row", Static).update("+35 BONUS")
            self.query_one("#bonus-hint-row", Static).update("")
        else:
            self.query_one("#bonus-row", Static).update("—")
            needed = 63 - subtotal
            hint = f"Need {needed} more for bonus" if needed > 0 else ""
            self.query_one("#bonus-hint-row", Static).update(hint)

        self.query_one("#total-row", Static).update(f"TOTAL:  {game.grand_total}")
