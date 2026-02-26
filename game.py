"""
GameState class for Yahtzee — tracks all mutable game data.

Provides roll, toggle_hold, commit, and reset methods, plus computed
properties for upper_subtotal, bonus, grand_total, and is_game_over.
"""

import random
import scoring

UPPER_CATEGORIES = ["ones", "twos", "threes", "fours", "fives", "sixes"]

ALL_CATEGORIES = [
    "ones", "twos", "threes", "fours", "fives", "sixes",
    "three_of_a_kind", "four_of_a_kind", "full_house",
    "small_straight", "large_straight", "yahtzee", "chance",
]

_SCORING_FUNCTIONS = {
    "ones": scoring.ones,
    "twos": scoring.twos,
    "threes": scoring.threes,
    "fours": scoring.fours,
    "fives": scoring.fives,
    "sixes": scoring.sixes,
    "three_of_a_kind": scoring.three_of_a_kind,
    "four_of_a_kind": scoring.four_of_a_kind,
    "full_house": scoring.full_house,
    "small_straight": scoring.small_straight,
    "large_straight": scoring.large_straight,
    "yahtzee": scoring.yahtzee,
    "chance": scoring.chance,
}


class GameState:
    """Tracks all mutable Yahtzee game data."""

    def __init__(self) -> None:
        self.dice: list[int] = [0, 0, 0, 0, 0]
        self.held: list[bool] = [False] * 5
        self.roll_count: int = 0
        self.scores: dict[str, int | None] = {cat: None for cat in ALL_CATEGORIES}
        self.game_over: bool = False

    def roll(self) -> None:
        """Randomize unheld dice and increment roll_count. No-op if roll_count >= 3."""
        if self.roll_count >= 3:
            return
        for i in range(5):
            if not self.held[i]:
                self.dice[i] = random.randint(1, 6)
        self.roll_count += 1

    def toggle_hold(self, index: int) -> None:
        """Flip held[index]. Only callable when roll_count >= 1; no-op otherwise."""
        if self.roll_count < 1:
            return
        self.held[index] = not self.held[index]

    def commit(self, category: str) -> None:
        """Store the current score for category and reset dice/held/roll_count.

        Raises ValueError if category already committed or roll_count == 0.
        """
        if category not in self.scores:
            raise ValueError(f"Unknown category: '{category}'.")
        if self.scores[category] is not None:
            raise ValueError(f"Category '{category}' already committed.")
        if self.roll_count == 0:
            raise ValueError("Cannot commit before rolling.")

        score_fn = _SCORING_FUNCTIONS[category]
        self.scores[category] = score_fn(self.dice)

        # Reset for the next turn
        self.dice = [0, 0, 0, 0, 0]
        self.held = [False] * 5
        self.roll_count = 0

        if self.is_game_over:
            self.game_over = True

    def reset(self) -> None:
        """Return all state to initial values."""
        self.dice = [0, 0, 0, 0, 0]
        self.held = [False] * 5
        self.roll_count = 0
        self.scores = {cat: None for cat in ALL_CATEGORIES}
        self.game_over = False

    @property
    def upper_subtotal(self) -> int:
        """Return the sum of committed Ones–Sixes scores."""
        return sum(
            self.scores[cat]
            for cat in UPPER_CATEGORIES
            if self.scores[cat] is not None
        )

    @property
    def bonus(self) -> int:
        """Return 35 if upper_subtotal >= 63, else 0."""
        return 35 if self.upper_subtotal >= 63 else 0

    @property
    def grand_total(self) -> int:
        """Return sum of all committed scores plus bonus."""
        committed = sum(s for s in self.scores.values() if s is not None)
        return committed + self.bonus

    @property
    def is_game_over(self) -> bool:
        """Return True when all 13 categories are committed."""
        return all(s is not None for s in self.scores.values())
