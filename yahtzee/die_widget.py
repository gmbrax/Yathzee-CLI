from textual.app import ComposeResult
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Static

# Pip layouts: 3 content rows × 5 chars each (no box borders; Textual CSS border provides the box)
DICE_FACES: dict[int, str] = {
    0: "     \n     \n     ",  # unrolled – blank
    1: "     \n  ●  \n     ",  # center
    2: " ●   \n     \n   ● ",  # top-left, bottom-right
    3: " ●   \n  ●  \n   ● ",  # diagonal
    4: " ● ● \n     \n ● ● ",  # four corners
    5: " ● ● \n  ●  \n ● ● ",  # corners + center
    6: " ● ● \n ● ● \n ● ● ",  # two columns of three
}


class DieWidget(Widget):
    """A single focusable die widget that renders a 5-row ASCII-style box with pip characters.

    States:
    - Unheld, unfocused: dim border
    - Held: double green border + 'HELD' label
    - Focused: accent-coloured border
    - Held + focused: double accent border + 'HELD' label
    """

    class ToggleHoldRequest(Message):
        """Posted when the player presses Space to toggle hold on this die."""

        def __init__(self, index: int) -> None:
            super().__init__()
            self.index = index

    BINDINGS = [("space", "toggle_hold", "Hold/Release")]

    can_focus = True

    value: reactive[int] = reactive(0)
    held: reactive[bool] = reactive(False)

    def __init__(self, index: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.die_index = index

    def compose(self) -> ComposeResult:
        yield Static(DICE_FACES[0], id=f"face-{self.die_index}")
        yield Label("", id=f"held-{self.die_index}")

    def watch_value(self, value: int) -> None:
        self.query_one(f"#face-{self.die_index}", Static).update(DICE_FACES[value])

    def watch_held(self, held: bool) -> None:
        self.query_one(f"#held-{self.die_index}", Label).update("HELD" if held else "")
        self.set_class(held, "held")

    def action_toggle_hold(self) -> None:
        self.post_message(self.ToggleHoldRequest(self.die_index))
