import os
from pathlib import Path
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, Center, Middle
from textual.screen import ModalScreen
from textual.widgets import DirectoryTree, Footer, Header, TextArea, Label, Markdown, Input

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

class Zenmark(App):
    """A minimalist, keyboard-centric daily planner."""

    CSS_PATH = "zenmarkdown.tcss"

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", show=True),
        Binding("ctrl+b", "toggle_sidebar", "Toggle Sidebar", show=True),
        Binding("ctrl+s", "save_file", "Save File", show=True),
        Binding("ctrl+m", "toggle_markdown", "Toggle Markdown", show=True),
        Binding("ctrl+n", "create_file", "Create File", show=True),
        Binding("ctrl+d", "delete_file", "Delete File", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.current_file: Path | None = None

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Horizontal():
            # The tree navigation sidebar
            yield DirectoryTree("/Users/brijanya/Documents/Code/python_scripts/textual_tutorial/zenmark.py/", id="tree")
            
            # The main text area mapped to markdown language
            with Vertical(id="editor-container"):
                self.text_area = TextArea(language="markdown", id="editor")
                self.text_area.show_line_numbers = True
                yield self.text_area
                self.markdown_viewer = Markdown(id="markdown")
                yield self.markdown_viewer
                yield Label("Ln 1, Col 1", id="cursor-pos")
        yield Footer()

    def on_mount(self) -> None:
        """Called when app starts."""
        self.dark = True  # Dark mode
        # Set initial text area content or leave it empty

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Called when the user selects a file in the directory tree."""
        event.stop()
        try:
            # We want to edit Markdown/Text files
            self.current_file = event.path
            with open(event.path, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_area.text = content
            self.sub_title = str(self.current_file.name)
        except Exception:
            # If it's a binary file or error reading, ignore or show error
            pass

    def on_text_area_selection_changed(self, event: TextArea.SelectionChanged) -> None:
        """Update cursor position when selection changes."""
        label = self.query_one("#cursor-pos", Label)
        row, col = event.selection.end
        label.update(f"Ln {row + 1}, Col {col + 1}")

    def action_toggle_sidebar(self) -> None:
        """Toggle the visibility of the directory tree sidebar (Focus Mode)."""
        tree = self.query_one(DirectoryTree)
        tree.display = not tree.display
        
    async def action_toggle_markdown(self) -> None:
        """Toggle between text editor and markdown preview."""
        if self.text_area.display:
            # Switch to markdown
            self.text_area.display = False
            self.markdown_viewer.display = True
            await self.markdown_viewer.update(self.text_area.text)
            self.query_one("#cursor-pos").display = False
        else:
            # Switch to text editor
            self.markdown_viewer.display = False
            self.text_area.display = True
            self.query_one("#cursor-pos").display = True
            self.text_area.focus()
            
    def action_save_file(self) -> None:
        """Save the current text area content to the active file."""
        if self.current_file and self.current_file.is_file():
            try:
                with open(self.current_file, "w", encoding="utf-8") as f:
                    f.write(self.text_area.text)
                # optionally show a notification
                self.notify("File saved successfully", timeout=2)
            except Exception as e:
                self.notify(f"Error saving file: {e}", severity="error", timeout=3)
        else:
            self.notify("No file selected to save.", severity="warning", timeout=2)

    def action_create_file(self) -> None:
        """Prompt to create a new file."""
        def check_and_create(filename: str | None) -> None:
            if not filename:
                return
            path = Path("/Users/brijanya/Documents/Code/python_scripts/textual_tutorial/zenmark.py/") / filename
            try:
                if path.exists():
                    self.notify(f"File {filename} already exists", severity="warning", timeout=3)
                    return
                with open(path, "w", encoding="utf-8") as f:
                    f.write("")
                self.notify(f"File '{filename}' created successfully", timeout=2)
                # Reload tree to show new file
                tree = self.query_one(DirectoryTree)
                tree.path = tree.path
            except Exception as e:
                self.notify(f"Error creating file: {e}", severity="error", timeout=3)

        self.push_screen(NewFileScreen(), check_and_create)

    def action_delete_file(self) -> None:
        """Prompt to delete the current file."""
        if self.current_file and self.current_file.is_file():
            def check_and_delete(confirm: bool | None) -> None:
                if confirm:
                    try:
                        self.current_file.unlink()
                        self.notify(f"File '{self.current_file.name}' deleted successfully.", timeout=2)
                        self.current_file = None
                        self.text_area.text = ""
                        self.sub_title = ""
                        # Reload tree to accurately reflect deleted file
                        tree = self.query_one(DirectoryTree)
                        tree.path = tree.path
                    except Exception as e:
                        self.notify(f"Error deleting file: {e}", severity="error", timeout=3)

            self.push_screen(ConfirmDeleteScreen(self.current_file.name), check_and_delete)
        else:
            self.notify("No file selected to delete.", severity="warning", timeout=2)

if __name__ == "__main__":
    app = Zenmark()
    app.run()
