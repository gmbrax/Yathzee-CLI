"""AboutScreen — About box modal overlay."""

import importlib.metadata
import sys
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.events import Key
from textual.screen import ModalScreen
from textual.widgets import Static

AUTHOR = "Gustavo Henrique Santos Souza de Miranda"


def _get_version() -> str:
    try:
        return importlib.metadata.version("yahtzee")
    except importlib.metadata.PackageNotFoundError:
        pass
    try:
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib  # type: ignore[no-redef]
        return tomllib.loads(Path("pyproject.toml").read_text())["project"]["version"]
    except Exception:
        pass
    return "0.1.0-dev"


class AboutScreen(ModalScreen):
    """About box overlay shown when A is pressed."""

    CSS = """
    AboutScreen {
        align: center middle;
    }
    #about-dialog {
        width: 50;
        height: auto;
        border: double #79c0ff;
        background: #16213e;
        padding: 1 2;
    }
    #about-title {
        text-align: center;
        color: #79c0ff;
        text-style: bold;
    }
    .about-line {
        text-align: center;
    }
    #about-hint {
        text-align: center;
        color: #8b949e;
    }
    """

    def compose(self) -> ComposeResult:
        version = _get_version()
        py = sys.version_info
        python_version = f"{py.major}.{py.minor}.{py.micro}"
        textual_version = importlib.metadata.version("textual")

        with Vertical(id="about-dialog"):
            yield Static("YAHTZEE", id="about-title")
            yield Static("")
            yield Static(f"Version: {version}", classes="about-line")
            yield Static(f"Author:  {AUTHOR}", classes="about-line")
            yield Static(f"Python:  {python_version}", classes="about-line")
            yield Static(f"Textual: {textual_version}", classes="about-line")
            yield Static("")
            yield Static("A classic dice game for the terminal.", classes="about-line")
            yield Static("")
            yield Static("Press Enter, Space, or Esc to close", id="about-hint")

    def on_key(self, event: Key) -> None:
        if event.key in ("escape", "enter", "space"):
            self.dismiss()
