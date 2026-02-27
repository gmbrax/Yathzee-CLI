import random

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Horizontal, Vertical

import scoring
from yahtzee.confirm_new_game_screen import ConfirmNewGameScreen
from yahtzee.die_widget import DieWidget
from yahtzee.game_over_screen import GameOverScreen
from yahtzee.quit_confirm_screen import QuitConfirmScreen
from yahtzee.scorecard_widget import CategoryRow, ScorecardWidget
from yahtzee.yahtzee_celebration_screen import YahtzeeCelebrationScreen
from game import GameState


class YahtzeeApp(App):
    CSS_PATH = "app.tcss"
    TITLE = "YAHTZEE"
    SUB_TITLE = "Roll 0/3"
    BINDINGS = [
        ("r", "roll", "Roll"),
        ("n", "new_game", "New Game"),
        ("q", "quit_confirm", "Quit"),
    ]

    def on_mount(self) -> None:
        self.game = GameState()
        self._animating: bool = False
        self._anim_timer = None
        self._anim_frame_count: int = 0
        self._anim_held: list[bool] = []
        self._anim_final: list[int] = []
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
        if self._animating:
            return
        if self.game.roll_count >= 3:
            return
        self.game.roll()
        self.sub_title = f"Roll {self.game.roll_count}/3"
        self._animating = True
        self._anim_frame_count = 0
        self._anim_held = list(self.game.held)
        self._anim_final = list(self.game.dice)
        self._anim_timer = self.set_interval(0.04, self._on_animation_frame)

    def _on_animation_frame(self) -> None:
        self._anim_frame_count += 1
        if self._anim_frame_count < 8:
            for i in range(5):
                if not self._anim_held[i]:
                    self.query_one(f"#die-{i}", DieWidget).value = random.randint(1, 6)
        else:
            self._anim_timer.stop()
            for i in range(5):
                self.query_one(f"#die-{i}", DieWidget).value = self._anim_final[i]
            self._animating = False
            self.query_one(ScorecardWidget).refresh_scores(self.game)
            if scoring.yahtzee(self.game.dice) == 50:
                self.push_screen(YahtzeeCelebrationScreen())

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
        if self._animating:
            return
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
        game_in_progress = any_committed or self.game.roll_count > 0
        if game_in_progress and not self.game.is_game_over:
            self.push_screen(ConfirmNewGameScreen(), self._handle_confirm_new_game)
        else:
            self._reset_game()

    def _handle_confirm_new_game(self, result: bool | None) -> None:
        if result:
            self._reset_game()

    def _handle_game_over(self, result: str | None) -> None:
        if result == "new_game":
            self._reset_game()
        elif result == "quit":
            self.exit()

    def action_quit_confirm(self) -> None:
        self.push_screen(QuitConfirmScreen(), self._handle_quit_confirm)

    def action_quit(self) -> None:
        self.push_screen(QuitConfirmScreen(), self._handle_quit_confirm)

    def _handle_quit_confirm(self, result: bool | None) -> None:
        if result:
            self.exit()

    def _reset_game(self) -> None:
        if self._animating:
            self._anim_timer.stop()
            self._animating = False
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
