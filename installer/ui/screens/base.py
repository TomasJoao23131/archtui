from textual.widgets import Static, Button, Input, SelectionList
from textual.containers import Container, Horizontal
from textual.binding import Binding
from installer.ui.sidebar import InstallerScreen


PACKAGES_BASE = [
    "base", "base-devel", "linux", "linux-firmware",
    "vim", "nano", "openssh", "networkmanager", "sudo",
]

PACKAGES_EXTRAS = [
    ("Firefox (navegador)", "firefox"),
    ("LibreOffice (escritório)", "libreoffice-fresh"),
    ("Servidor Xorg", "xorg"),
    ("Sway (compositor Wayland)", "sway"),
]


class BaseSystemScreen(InstallerScreen):
    """Passo 4 — Hostname e pacotes."""

    STEP_NUMBER = 4
    STEP_NAME = "Sistema Base"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Passo 4 — Sistema Base", id="header-text"),
            Static(
                "Defina o hostname e escolha pacotes extras.\n"
                "Tab para navegar entre campos. Espaço para selecionar extras.",
                classes="help-text",
            ),
            Static("Hostname (nome na rede):", classes="field-label"),
            Input(placeholder="archlinux", id="hostname-input", value="archlinux"),
            Static("Pacotes base (sempre instalados):", classes="field-label"),
            Container(
                *[Static(f" • {p}", classes="package-item") for p in PACKAGES_BASE],
                id="packages-box",
            ),
            Static("Extras (Espaço = selecionar):", classes="field-label"),
            SelectionList(*PACKAGES_EXTRAS, id="extras-list"),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            hostname = self.query_one("#hostname-input", Input)
            extras = self.get_selected_values("#extras-list")
            self.app.config["hostname"] = hostname.value.strip() or "archlinux"
            self.app.config["packages"] = PACKAGES_BASE[:]
            self.app.config["extra_packages"] = extras
            self.go_next("bootloader")
        elif event.button.id == "btn-back":
            self.go_back("partition")

    def action_go_back(self) -> None:
        self.go_back("partition")
