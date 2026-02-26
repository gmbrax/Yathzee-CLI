"""
██╗   ██╗ █████╗ ██╗  ██╗████████╗███████╗███████╗
╚██╗ ██╔╝██╔══██╗██║  ██║╚══██╔══╝╚════██║██╔════╝
 ╚████╔╝ ███████║███████║   ██║       ██╔╝█████╗
  ╚██╔╝  ██╔══██║██╔══██║   ██║      ██╔╝ ██╔══╝
   ██║   ██║  ██║██║  ██║   ██║      ██║  ███████╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝      ╚═╝  ╚══════╝

Yahtzee in Python Textual — because why not?
"""

import random
from collections import Counter
from textual.app import App, ComposeResult
from textual.widgets import Button, Label, Static, Footer, Header
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.message import Message
from textual.css.query import NoMatches


DICE_FACES = {
    1: "╔═════╗\n║     ║\n║  ●  ║\n║     ║\n╚═════╝",
    2: "╔═════╗\n║ ●   ║\n║     ║\n║   ● ║\n╚═════╝",
    3: "╔═════╗\n║ ●   ║\n║  ●  ║\n║   ● ║\n╚═════╝",
    4: "╔═════╗\n║ ● ● ║\n║     ║\n║ ● ● ║\n╚═════╝",
    5: "╔═════╗\n║ ● ● ║\n║  ●  ║\n║ ● ● ║\n╚═════╝",
    6: "╔═════╗\n║ ● ● ║\n║ ● ● ║\n║ ● ● ║\n╚═════╝",
    0: "╔═════╗\n║░░░░░║\n║░░░░░║\n║░░░░░║\n╚═════╝",
}

CATEGORIES = [
    ("ones",           "[A] Ones",           "upper", "a"),
    ("twos",           "[B] Twos",           "upper", "b"),
    ("threes",         "[C] Threes",         "upper", "c"),
    ("fours",          "[D] Fours",          "upper", "d"),
    ("fives",          "[E] Fives",          "upper", "e"),
    ("sixes",          "[F] Sixes",          "upper", "f"),
    ("three_of_kind",  "[G] Three of a Kind","lower", "g"),
    ("four_of_kind",   "[H] Four of a Kind", "lower", "h"),
    ("full_house",     "[I] Full House",     "lower", "i"),
    ("sm_straight",    "[J] Sm. Straight",   "lower", "j"),
    ("lg_straight",    "[K] Lg. Straight",   "lower", "k"),
    ("yahtzee",        "[L] YAHTZEE!",       "lower", "l"),
    ("chance",         "[M] Chance",         "lower", "m"),
]

# Map keys to category names
KEY_TO_CATEGORY = {cat[3]: cat[0] for cat in CATEGORIES}


def calc_score(category: str, dice: list[int]) -> int:
    if not dice:
        return 0
    counts = Counter(dice)
    total = sum(dice)
    vals = sorted(counts.keys())

    match category:
        case "ones":   return counts.get(1, 0) * 1
        case "twos":   return counts.get(2, 0) * 2
        case "threes": return counts.get(3, 0) * 3
        case "fours":  return counts.get(4, 0) * 4
        case "fives":  return counts.get(5, 0) * 5
        case "sixes":  return counts.get(6, 0) * 6
        case "three_of_kind":
            return total if any(v >= 3 for v in counts.values()) else 0
        case "four_of_kind":
            return total if any(v >= 4 for v in counts.values()) else 0
        case "full_house":
            return 25 if sorted(counts.values()) == [2, 3] else 0
        case "sm_straight":
            sets = [frozenset([1,2,3,4]), frozenset([2,3,4,5]), frozenset([3,4,5,6])]
            return 30 if any(s.issubset(set(dice)) for s in sets) else 0
        case "lg_straight":
            return 40 if set(dice) in [frozenset([1,2,3,4,5]), frozenset([2,3,4,5,6])] else 0
        case "yahtzee":
            return 50 if len(counts) == 1 else 0
        case "chance":
            return total
        case _:
            return 0


class DieWidget(Static):
    """A single die that can be toggled (held) via keyboard."""

    held = reactive(False)

    class Toggled(Message):
        def __init__(self, index: int) -> None:
            self.index = index
            super().__init__()

    def __init__(self, index: int, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self._value = 0

    def compose(self) -> ComposeResult:
        yield Static(DICE_FACES[0], id=f"die_face_{self.index}")
        yield Label(f"[{self.index + 1}]", id=f"die_label_{self.index}")

    def update_value(self, value: int) -> None:
        self._value = value
        self.query_one(f"#die_face_{self.index}", Static).update(DICE_FACES[value])

    def watch_held(self, held: bool) -> None:
        label = self.query_one(f"#die_label_{self.index}", Label)
        label.update("🔒 HELD" if held else f"[{self.index + 1}]")
        self.add_class("held") if held else self.remove_class("held")

    def toggle(self) -> None:
        """Toggle held state via keyboard."""
        if self._value > 0:
            self.held = not self.held
            self.post_message(self.Toggled(self.index))


class ScoreRow(Static):
    """A score row in the scorecard, selectable via keyboard."""

    class Selected(Message):
        def __init__(self, category: str) -> None:
            self.category = category
            super().__init__()

    def __init__(self, category: str, label: str, **kwargs):
        super().__init__(**kwargs)
        self.category = category
        self._label = label
        self._score: int | None = None
        self._preview: int | None = None

    def compose(self) -> ComposeResult:
        yield Label(f"{self._label:<16}", id=f"cat_label_{self.category}")
        yield Label("---", id=f"cat_score_{self.category}")

    def set_preview(self, score: int | None) -> None:
        self._preview = score
        lbl = self.query_one(f"#cat_score_{self.category}", Label)
        if self._score is not None:
            return
        if score is not None:
            lbl.update(f"[dim]{score:>3}[/dim]")
            self.add_class("previewable")
        else:
            lbl.update("---")
            self.remove_class("previewable")

    def set_score(self, score: int) -> None:
        self._score = score
        self._preview = None
        lbl = self.query_one(f"#cat_score_{self.category}", Label)
        lbl.update(f"[bold]{score:>3}[/bold]")
        self.add_class("scored")
        self.remove_class("previewable")

    def select(self) -> bool:
        """Select this category via keyboard. Returns True if successful."""
        if self._score is None and self._preview is not None:
            self.post_message(self.Selected(self.category))
            return True
        return False


class YahtzeeApp(App):
    CSS = """
    Screen {
        background: #0d1117;
        color: #e6edf3;
    }

    Header {
        background: #1c2a3a;
        color: #58a6ff;
        text-style: bold;
    }

    Footer {
        background: #1c2a3a;
        color: #8b949e;
    }

    #main-layout {
        layout: horizontal;
        height: 1fr;
    }

    #left-panel {
        width: 42;
        padding: 1;
        border: solid #30363d;
        background: #161b22;
    }

    #right-panel {
        width: 1fr;
        padding: 1;
    }

    /* ── DICE ── */
    #dice-area {
        layout: horizontal;
        height: auto;
        margin-bottom: 1;
    }

    DieWidget {
        width: 9;
        height: 8;
        border: solid #30363d;
        background: #1c2a3a;
        margin: 0 1;
        padding: 0;
        content-align: center middle;
    }

    DieWidget:hover {
        border: solid #58a6ff;
    }

    DieWidget.held {
        border: solid #3fb950;
        background: #0f2915;
    }

    DieWidget > Label {
        text-align: center;
        color: #3fb950;
        text-style: bold;
        width: 1fr;
    }

    DieWidget > Static {
        color: #e6edf3;
        text-align: center;
        width: 1fr;
    }

    /* ── BUTTONS ── */
    #controls {
        layout: horizontal;
        height: auto;
        margin-bottom: 1;
    }

    Button {
        margin: 0 1;
    }

    #btn-roll {
        background: #1f6feb;
        color: white;
        border: none;
    }

    #btn-roll:hover {
        background: #388bfd;
    }

    #btn-roll:disabled {
        background: #21262d;
        color: #484f58;
    }

    #btn-new {
        background: #238636;
        color: white;
        border: none;
    }

    #btn-new:hover {
        background: #2ea043;
    }

    /* ── INFO ── */
    #rolls-label {
        color: #f0883e;
        text-style: bold;
        margin-bottom: 1;
    }

    #status-label {
        color: #8b949e;
        margin-bottom: 1;
    }

    /* ── SCORECARD ── */
    #scorecard-title {
        text-style: bold;
        color: #58a6ff;
        border-bottom: solid #30363d;
        padding-bottom: 1;
        margin-bottom: 1;
    }

    #section-upper, #section-lower {
        margin-bottom: 1;
    }

    .section-header {
        color: #8b949e;
        text-style: italic;
        margin-bottom: 0;
    }

    ScoreRow {
        layout: horizontal;
        height: 1;
        padding: 0 1;
    }

    ScoreRow:hover {
        background: #1c2a3a;
    }

    ScoreRow.previewable {
        background: #1a2332;
    }

    ScoreRow.previewable:hover {
        background: #1f3a52;
    }

    ScoreRow.scored {
        color: #8b949e;
    }

    ScoreRow > Label:first-child {
        width: 1fr;
    }

    ScoreRow > Label:last-child {
        width: 6;
        text-align: right;
    }

    #bonus-row {
        layout: horizontal;
        height: 1;
        padding: 0 1;
        color: #f0883e;
    }

    #bonus-row > Label:first-child { width: 1fr; }
    #bonus-row > Label:last-child  { width: 6; text-align: right; }

    #total-row {
        layout: horizontal;
        height: 2;
        padding: 0 1;
        border-top: solid #30363d;
        color: #ffa657;
        text-style: bold;
    }

    #total-row > Label:first-child { width: 1fr; }
    #total-row > Label:last-child  { width: 6; text-align: right; }

    /* ── GAME OVER ── */
    #gameover-overlay {
        display: none;
        align: center middle;
        background: rgba(0,0,0,0.8);
        layer: overlay;
    }

    #gameover-box {
        width: 40;
        height: 12;
        background: #1c2a3a;
        border: double #f0883e;
        padding: 2 4;
        content-align: center middle;
    }
    """

    TITLE = "🎲 YAHTZEE — Textual Edition (Keyboard Only)"
    BINDINGS = [
        ("r", "roll", "Roll"),
        ("n", "new_game", "New Game"),
        ("1", "toggle_die(0)", "Die 1"),
        ("2", "toggle_die(1)", "Die 2"),
        ("3", "toggle_die(2)", "Die 3"),
        ("4", "toggle_die(3)", "Die 4"),
        ("5", "toggle_die(4)", "Die 5"),
        ("a", "select_category('a')", "Ones"),
        ("b", "select_category('b')", "Twos"),
        ("c", "select_category('c')", "Threes"),
        ("d", "select_category('d')", "Fours"),
        ("e", "select_category('e')", "Fives"),
        ("f", "select_category('f')", "Sixes"),
        ("g", "select_category('g')", "3 of Kind"),
        ("h", "select_category('h')", "4 of Kind"),
        ("i", "select_category('i')", "Full House"),
        ("j", "select_category('j')", "Sm Straight"),
        ("k", "select_category('k')", "Lg Straight"),
        ("l", "select_category('l')", "Yahtzee"),
        ("m", "select_category('m')", "Chance"),
    ]

    def __init__(self):
        super().__init__()
        self.dice_values = [0, 0, 0, 0, 0]
        self.held = [False] * 5
        self.rolls_left = 3
        self.scores: dict[str, int] = {}
        self.turn_active = False

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="main-layout"):
            # Left: dice + controls + status
            with Vertical(id="right-panel"):
                yield Label("🎲 Press R to roll! Use 1-5 to hold, A-M to score", id="status-label")
                yield Label("Rolls left: 3", id="rolls-label")
                with Horizontal(id="dice-area"):
                    for i in range(5):
                        yield DieWidget(i, id=f"die_{i}")
                with Horizontal(id="controls"):
                    yield Button("🎲 ROLL (R)", id="btn-roll", variant="primary")
                    yield Button("🔄 New Game (N)", id="btn-new", variant="success")

            # Right: scorecard
            with Vertical(id="left-panel"):
                yield Label("📋 SCORECARD", id="scorecard-title")
                with Vertical(id="section-upper"):
                    yield Label("── Upper Section ──", classes="section-header")
                    for cat, lbl, sec, _ in CATEGORIES:
                        if sec == "upper":
                            yield ScoreRow(cat, lbl, id=f"row_{cat}")
                    with Horizontal(id="bonus-row"):
                        yield Label("Bonus (≥63 → +35)")
                        yield Label("---", id="bonus-label")
                with Vertical(id="section-lower"):
                    yield Label("── Lower Section ──", classes="section-header")
                    for cat, lbl, sec, _ in CATEGORIES:
                        if sec == "lower":
                            yield ScoreRow(cat, lbl, id=f"row_{cat}")
                with Horizontal(id="total-row"):
                    yield Label("TOTAL")
                    yield Label("0", id="total-label")

        yield Footer()

    def action_roll(self) -> None:
        self._do_roll()

    def action_new_game(self) -> None:
        self._new_game()

    def action_toggle_die(self, index: int) -> None:
        """Toggle held state for a die."""
        if self.turn_active:
            die = self.query_one(f"#die_{index}", DieWidget)
            die.toggle()

    def action_select_category(self, key: str) -> None:
        """Select a scoring category by key."""
        if not self.turn_active:
            return
        category = KEY_TO_CATEGORY.get(key)
        if category:
            row = self.query_one(f"#row_{category}", ScoreRow)
            row.select()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-roll":
            self._do_roll()
        elif event.button.id == "btn-new":
            self._new_game()

    def on_die_widget_toggled(self, event: DieWidget.Toggled) -> None:
        self.held[event.index] = self.query_one(f"#die_{event.index}", DieWidget).held

    def on_score_row_selected(self, event: ScoreRow.Selected) -> None:
        if not self.turn_active:
            return
        score = calc_score(event.category, self.dice_values)
        self.scores[event.category] = score
        self.query_one(f"#row_{event.category}", ScoreRow).set_score(score)
        self._clear_previews()
        self._update_totals()
        self._start_new_turn()

        if len(self.scores) == len(CATEGORIES):
            self._game_over()

    def _do_roll(self) -> None:
        if self.rolls_left <= 0:
            return

        self.turn_active = True

        for i in range(5):
            if not self.held[i]:
                self.dice_values[i] = random.randint(1, 6)
                self.query_one(f"#die_{i}", DieWidget).update_value(self.dice_values[i])

        self.rolls_left -= 1
        self.query_one("#rolls-label", Label).update(
            f"Rolls left: [bold]{self.rolls_left}[/bold]"
        )

        if self.rolls_left == 0:
            self.query_one("#btn-roll", Button).disabled = True
            self.query_one("#status-label", Label).update(
                "✅ No more rolls — press A-M to pick a category!"
            )
        else:
            self.query_one("#status-label", Label).update(
                "🔒 Press 1-5 to hold dice, R to roll, A-M to score"
            )

        self._show_previews()

    def _show_previews(self) -> None:
        for cat, _, _, _ in CATEGORIES:
            if cat not in self.scores:
                score = calc_score(cat, self.dice_values)
                self.query_one(f"#row_{cat}", ScoreRow).set_preview(score)

    def _clear_previews(self) -> None:
        for cat, _, _, _ in CATEGORIES:
            if cat not in self.scores:
                try:
                    self.query_one(f"#row_{cat}", ScoreRow).set_preview(None)
                except NoMatches:
                    pass

    def _update_totals(self) -> None:
        upper_cats = [c for c, _, s, _ in CATEGORIES if s == "upper"]
        upper_sum = sum(self.scores.get(c, 0) for c in upper_cats)
        bonus = 35 if upper_sum >= 63 else 0
        total = sum(self.scores.values()) + bonus

        self.query_one("#bonus-label", Label).update(
            f"[bold]{bonus}[/bold]" if bonus else "---"
        )
        self.query_one("#total-label", Label).update(f"{total}")

    def _start_new_turn(self) -> None:
        self.held = [False] * 5
        self.rolls_left = 3
        self.dice_values = [0, 0, 0, 0, 0]
        self.turn_active = False

        for i in range(5):
            die = self.query_one(f"#die_{i}", DieWidget)
            die.held = False
            die.update_value(0)

        self.query_one("#rolls-label", Label).update("Rolls left: [bold]3[/bold]")
        self.query_one("#btn-roll", Button).disabled = False
        self.query_one("#status-label", Label).update(
            "🎲 Press R to roll the dice!"
        )

    def _new_game(self) -> None:
        self.scores = {}
        self._start_new_turn()
        self._clear_previews()
        self._update_totals()
        self.query_one("#bonus-label", Label).update("---")

        for cat, _, _, _ in CATEGORIES:
            try:
                row = self.query_one(f"#row_{cat}", ScoreRow)
                row._score = None
                row._preview = None
                row.remove_class("scored")
                row.remove_class("previewable")
                row.query_one(f"#cat_score_{cat}", Label).update("---")
            except NoMatches:
                pass

    def _game_over(self) -> None:
        upper_cats = [c for c, _, s, _ in CATEGORIES if s == "upper"]
        upper_sum = sum(self.scores.get(c, 0) for c in upper_cats)
        bonus = 35 if upper_sum >= 63 else 0
        total = sum(self.scores.values()) + bonus

        self.query_one("#status-label", Label).update(
            f"🏆 GAME OVER! Final score: [bold]{total}[/bold] — Press N for a new game!"
        )
        self.query_one("#btn-roll", Button).disabled = True


if __name__ == "__main__":
    app = YahtzeeApp()
    app.run()
