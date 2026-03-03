import os
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import DirectoryTree, Footer, Header, TextArea, Label, Markdown

from time import sleep


class Zenmark(App):
    """A minimalist, keyboard-centric daily planner."""

    CSS_PATH = "zenmarkdown.tcss"

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", show=True),
        Binding("ctrl+b", "toggle_sidebar", "Toggle Sidebar", show=True),
        Binding("ctrl+s", "save_file", "Save File", show=True),
        Binding("ctrl+m", "toggle_markdown", "Toggle Markdown", show=True),
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
                self.text_area = TextArea(language="python", id="editor")
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


if __name__ == "__main__":
    app = Zenmark()
    app.run()
