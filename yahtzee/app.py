from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Horizontal, Vertical

from yahtzee.die_widget import DieWidget


class YahtzeeApp(App):
    CSS_PATH = "app.tcss"
    TITLE = "YAHTZEE"
    SUB_TITLE = "Roll 0/3"
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main-layout"):
            with Vertical(id="dice-panel"):
                with Horizontal(id="dice-row"):
                    for i in range(5):
                        yield DieWidget(i, id=f"die-{i}")
            with Vertical(id="scorecard-panel"):
                pass
        yield Footer()


if __name__ == "__main__":
    app = YahtzeeApp()
    app.run()
