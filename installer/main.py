from pathlib import Path

from textual.app import App

from installer.ui.screens import (
    WelcomeScreen,
    LanguageScreen,
    KeyboardScreen,
    PartitionScreen,
    BaseSystemScreen,
    BootloaderScreen,
    UserScreen,
    DesktopScreen,
    SummaryScreen,
    InstallationScreen,
)


class ArchTUI(App):
    """Instalador do Arch Linux com interface TUI."""

    TITLE = "ArchTUI — Instalador do Arch Linux"

    CSS_PATH = Path(__file__).parent / "ui" / "styles.tcss"

    SCREENS = {
        "welcome": WelcomeScreen,
        "language": LanguageScreen,
        "keyboard": KeyboardScreen,
        "partition": PartitionScreen,
        "base": BaseSystemScreen,
        "bootloader": BootloaderScreen,
        "user": UserScreen,
        "desktop": DesktopScreen,
        "summary": SummaryScreen,
        "installation": InstallationScreen,
    }

    def __init__(self):
        super().__init__()
        self.config = {}
        self.state = {"step": 0}

    def on_mount(self) -> None:
        self.push_screen("welcome")
