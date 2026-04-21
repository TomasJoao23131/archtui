from textual.widgets import Static, Button, Input, SelectionList
from textual.containers import Container, Horizontal, Vertical
from installer.ui.sidebar import InstallerScreen


PACKAGES_BASE = [
    "base",
    "base-devel",
    "linux",
    "linux-firmware",
    "vim",
    "nano",
    "openssh",
    "networkmanager",
    "sudo",
]

PACKAGES_EXTRAS = [
    ("Gestor de janelas Sway", "sway"),
    ("Escritorio LibreOffice", "libreoffice-fresh"),
    ("Navegador Firefox", "firefox"),
    ("Servidor Xorg", "xorg"),
]


class BaseSystemScreen(InstallerScreen):
    STEP_NUMBER = 4
    STEP_NAME = "Sistema Base"

    def compose(self):
        content = Container(
            Static("Configurar Sistema Base", id="header-text"),
            Static("Hostname (nome do computador):", id="hostname-label"),
            Input(placeholder="archlinux", id="hostname-input"),
            Static("Pacotes base a instalar:", id="packages-label"),
            Vertical(
                *[Static(f"  - {pkg}") for pkg in PACKAGES_BASE],
                id="packages-list"
            ),
            Static("Pacotes extras (opcional):", id="extras-label"),
            SelectionList(*PACKAGES_EXTRAS, id="extras-list"),
            Horizontal(
                Button("Anterior", id="btn-back", variant="default"),
                Button("Seguinte", id="btn-next", variant="primary"),
                id="nav-buttons"
            ),
            id="base-container"
        )
        yield from self.compose_with_sidebar(content)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            hostname = self.query_one("#hostname-input", Input)
            extras = self.get_selected_values("#extras-list")
            self.app.config["hostname"] = hostname.value or "archlinux"
            self.app.config["packages"] = PACKAGES_BASE[:]
            self.app.config["extra_packages"] = extras
            self.app.push_screen("bootloader")
        elif event.button.id == "btn-back":
            self.app.pop_screen()
