"""RulesScreen — scrollable rules modal overlay."""

from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.events import Key
from textual.screen import ModalScreen
from textual.widgets import Markdown, Static


class RulesScreen(ModalScreen):
    """Scrollable rules overlay shown when ? is pressed."""

    CSS = """
    RulesScreen {
        align: center middle;
    }
    #rules-dialog {
        width: 80%;
        height: 90%;
        border: round #3fb950;
        background: #16213e;
        padding: 1 2;
    }
    #rules-scroll {
        height: 1fr;
    }
    #rules-hint {
        height: auto;
        text-align: center;
        color: #8b949e;
        padding-top: 1;
    }
    """

    def compose(self) -> ComposeResult:
        rules_path = Path(__file__).parent / "assets" / "rules.md"
        rules_content = rules_path.read_text()
        with Vertical(id="rules-dialog"):
            with VerticalScroll(id="rules-scroll"):
                yield Markdown(rules_content)
            yield Static("  ↑/↓ scroll  ·  Esc or ? close  ", id="rules-hint")

    def on_key(self, event: Key) -> None:
        if event.key in ("escape", "question_mark"):
            self.dismiss()
