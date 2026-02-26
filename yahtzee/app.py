from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Horizontal, Vertical

from yahtzee.die_widget import DieWidget
from yahtzee.scorecard_widget import ScorecardWidget
from game import GameState


class YahtzeeApp(App):
    CSS_PATH = "app.tcss"
    TITLE = "YAHTZEE"
    SUB_TITLE = "Roll 0/3"
    BINDINGS = [
        ("r", "roll", "Roll"),
        ("q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.game = GameState()
        self.query_one(ScorecardWidget).refresh_scores(self.game)

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main-layout"):
            with Vertical(id="dice-panel"):
                with Horizontal(id="dice-row"):
                    for i in range(5):
                        yield DieWidget(i, id=f"die-{i}")
            with Vertical(id="scorecard-panel"):
                yield ScorecardWidget(id="scorecard")
        yield Footer()

    def action_roll(self) -> None:
        self.game.roll()
        for i in range(5):
            self.query_one(f"#die-{i}", DieWidget).value = self.game.dice[i]
        self.sub_title = f"Roll {self.game.roll_count}/3"
        self.query_one(ScorecardWidget).refresh_scores(self.game)

    def on_die_widget_toggle_hold_request(
        self, event: DieWidget.ToggleHoldRequest
    ) -> None:
        self.game.toggle_hold(event.index)
        self.query_one(f"#die-{event.index}", DieWidget).held = self.game.held[
            event.index
        ]


if __name__ == "__main__":
    app = YahtzeeApp()
    app.run()
