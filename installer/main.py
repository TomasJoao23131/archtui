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
    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-columns: 32 1fr;
    }

    #sidebar {
        width: 32;
        min-width: 32;
        background: $surface;
        border-right: solid $border;
        padding: 1;
    }

    #main {
        width: 1fr;
        height: 100%;
        padding: 2;
    }

    #title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    #header-text {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    #welcome-container {
        height: 100%;
        column-span: 2;
        align: center middle;
    }

    #welcome-text {
        margin: 2 0;
        max-width: 60;
    }

    #buttons {
        width: 100%;
        content-align: center middle;
    }

    #language-container,
    #keyboard-container,
    #partition-container,
    #base-container,
    #bootloader-container,
    #user-container,
    #desktop-container,
    #summary-container,
    #install-container {
        height: 100%;
        layout: vertical;
        column-span: 2;
    }

    #nav-buttons {
        width: 100%;
        align: right bottom;
        padding-top: 1;
    }

    #help-text,
    #bootloader-help,
    #partition-help,
    #extras-label,
    #packages-label,
    #packages-list,
    #extras-label,
    #disk-label,
    #hostname-label,
    #username-label,
    #password-label,
    #password-confirm-label,
    #root-label,
    #method-label,
    #video-label,
    #multilib-label {
        margin-bottom: 1;
        color: $text-muted;
    }

    #progress {
        margin: 1 0;
    }

    #status-text {
        text-style: bold;
    }

    #detail-text {
        margin-bottom: 1;
    }

    #log-output {
        height: 1fr;
        border: round $border;
        padding: 1;
        overflow-y: auto;
    }

    Button {
        margin-left: 1;
    }

    OptionList {
        height: 10;
        margin-bottom: 1;
    }

    ListView {
        height: 10;
        margin-bottom: 1;
    }

    Input {
        margin-bottom: 1;
    }

    SelectionList {
        height: 8;
        margin-bottom: 1;
    }

    Switch {
        margin-bottom: 1;
    }
    """

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
