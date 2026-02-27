from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Horizontal, Vertical

from yahtzee.confirm_new_game_screen import ConfirmNewGameScreen
from yahtzee.die_widget import DieWidget
from yahtzee.game_over_screen import GameOverScreen
from yahtzee.scorecard_widget import CategoryRow, ScorecardWidget
from game import GameState


class YahtzeeApp(App):
    CSS_PATH = "app.tcss"
    TITLE = "YAHTZEE"
    SUB_TITLE = "Roll 0/3"
    BINDINGS = [
        ("r", "roll", "Roll"),
        ("n", "new_game", "New Game"),
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

    def on_category_row_commit_request(
        self, event: CategoryRow.CommitRequest
    ) -> None:
        if self.game.roll_count < 1:
            return
        self.game.commit(event.key)
        for i in range(5):
            die = self.query_one(f"#die-{i}", DieWidget)
            die.value = 0
            die.held = False
        self.sub_title = "Roll 0/3"
        self.query_one(ScorecardWidget).refresh_scores(self.game)
        if self.game.is_game_over:
            self.push_screen(
                GameOverScreen(self.game.grand_total, self.game.bonus > 0),
                self._handle_game_over,
            )
        else:
            self.query_one("#die-0").focus()

    def action_new_game(self) -> None:
        any_committed = any(v is not None for v in self.game.scores.values())
        if any_committed and not self.game.is_game_over:
            self.push_screen(ConfirmNewGameScreen(), self._handle_confirm_new_game)
        else:
            self._reset_game()

    def _handle_confirm_new_game(self, result: bool | None) -> None:
        if result:
            self._reset_game()

    def _handle_game_over(self, result: bool | None) -> None:
        if result:
            self._reset_game()

    def _reset_game(self) -> None:
        self.game.reset()
        for i in range(5):
            die = self.query_one(f"#die-{i}", DieWidget)
            die.value = 0
            die.held = False
        self.sub_title = "Roll 0/3"
        self.query_one(ScorecardWidget).refresh_scores(self.game)
        self.query_one("#die-0").focus()


if __name__ == "__main__":
    app = YahtzeeApp()
    app.run()
