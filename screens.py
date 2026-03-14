from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, Center, Middle
from textual.screen import ModalScreen
from textual.widgets import Label, Input

class NewFileScreen(ModalScreen[str]):
    """Screen that asks for a new file name."""

    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def compose(self) -> ComposeResult:
        with Center():
            with Middle():
                yield Vertical(
                    Label("Enter new file name:"),
                    Input(placeholder="filename.md", id="new-file-input"),
                    id="new-file-dialog"
                )

    def on_mount(self) -> None:
        # Style the dialog dynamically
        dialog = self.query_one("#new-file-dialog")
        dialog.styles.width = 40
        dialog.styles.height = "auto"
        dialog.styles.border = ("thick", "white")
        dialog.styles.background = "black"
        self.query_one(Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """When user hits enter in the input."""
        self.dismiss(event.value)

    def action_cancel(self) -> None:
        """When user presses escape."""
        self.dismiss(None)

class ConfirmDeleteScreen(ModalScreen[bool]):
    """Screen that asks for confirmation to delete a file."""

    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename

    BINDINGS = [
        Binding("y", "confirm", "Yes"),
        Binding("n", "cancel", "No"),
        Binding("escape", "cancel", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        with Center():
            with Middle():
                yield Vertical(
                    Label(f"Are you sure you want to delete '{self.filename}'? (y/n)"),
                    id="delete-dialog"
                )

    def on_mount(self) -> None:
        # Style the dialog dynamically
        dialog = self.query_one("#delete-dialog")
        dialog.styles.width = "auto"
        dialog.styles.height = "auto"
        dialog.styles.border = ("thick", "red")
        dialog.styles.background = "black"

    def action_confirm(self) -> None:
        self.dismiss(True)

    def action_cancel(self) -> None:
        self.dismiss(False)
