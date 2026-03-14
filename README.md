# Zenmark

A minimalist, keyboard-centric Markdown editor for your terminal.

## Features
- **Distraction-Free Environment**: Focus on writing with a minimalist UI hiding everything but the text.
- **File Management**: Create, delete, and save Markdown files instantly from your terminal.
- **File Sidebar**: Easily navigate through your workspace directory. Toggle visibility for True "Focus Mode".
- **Markdown Preview**: Enjoy a split-screen view with a text editor on the left and a live-updating Markdown preview on the right.
- **Keyboard-Centric Design**: Quick shortcuts to navigate and control the app without ever touching the mouse.

## Requirements
- Python 3.8+
- [Textual](https://textual.textualize.io/)

## Installation
1. Clone or download this project.
2. Install the required dependencies:
   ```bash
   pip install textual
   ```

## Usage
Run the application from your terminal:
```bash
python zenmarkdown.py
```

### Keyboard Shortcuts
- `Ctrl + Q`: Quit the application
- `Ctrl + B`: Toggle Sidebar (Focus Mode)
- `Ctrl + S`: Save the current file
- `Ctrl + N`: Create a new file
- `Ctrl + D`: Delete the currently selected file

## Customization
You can customize the styling of the application by editing the `zenmarkdown.tcss` file. By default, Zenmark comes with a dark mode theme that you can expand upon.
