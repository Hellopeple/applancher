import subprocess
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, Footer, Header, Log


class Apps(Horizontal):
    """Container for the application launcher buttons."""
    
    def compose(self) -> ComposeResult:
        yield Button("neofetch", id="neofetch", variant="primary")
        yield Button("ip a", id="ipa", variant="primary")
        yield Button("clock", id="clock", variant="primary")
        yield Button("calc", id="calculator", variant="primary")


class LauncherApp(App):
    """A Textual app to launch commands."""

    CSS_PATH = "applancher.tcss"

    BINDINGS = [
        ("e", "toggle_hide", "Back"),
        ("q", "quit()", "Quit")
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        self.apps = Apps()
        yield self.apps
        self.output_log = Log(id="output")
        yield self.output_log
        yield Footer()

    def on_mount(self) -> None:
        self.theme = "solarized-light"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handles button clicks and runs the selected command."""
        button_id = event.button.id
        if button_id == "neofetch":
            self.run_command(["neofetch"])
        elif button_id == "ipa":
            self.run_command(["ip", "a"])
        elif button_id == "calculator":
            self.run_command(["gnome-calculator"])  # Adjust if needed
        elif button_id == "clock":
            self.run_command(["echo", "dam sun"])  # Example clock app

    def run_command(self, command):
        """Run a shell command and display its output in the Log widget."""
        try:
            self.apps.display = False
            self.output_log.display = True
            self.output_log.clear()
            result = subprocess.run(command, text=True, capture_output=True)
            self.output_log.write(result.stdout or result.stderr)
        except FileNotFoundError:
            self.output_log.write(f"Command not found: {' '.join(command)}")

    
        

    def action_toggle_hide(self) -> None:
        """Toggle visibility of the Apps container."""
        self.apps.display = True
        self.output_log.display = False


if __name__ == "__main__":
    app = LauncherApp()
    app.run()
