from textual.widgets import Static, Button, Input, SelectionList
from textual.containers import Container, Horizontal
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
    ("LibreOffice (escritório)", "libreoffice-fresh"),
    ("Firefox (navegador web)", "firefox"),
    ("Servidor Xorg (necessário para alguns ambientes)", "xorg"),
]


class BaseSystemScreen(InstallerScreen):
    """Passo 4 — Configuração do sistema base."""

    STEP_NUMBER = 4
    STEP_NAME = "Sistema Base"

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Passo 4 — Sistema Base", id="header-text"),
            Static(
                "Configure o nome do computador e os pacotes a instalar.\n"
                "Os pacotes base são obrigatórios. Pode adicionar extras opcionais.",
                classes="help-text",
            ),
            Static("Hostname (nome do computador na rede):", classes="field-label"),
            Input(placeholder="archlinux", id="hostname-input"),
            Static("Pacotes base (sempre instalados):", classes="field-label"),
            Container(
                *[Static(f"  • {pkg}", classes="package-item") for pkg in PACKAGES_BASE],
                id="packages-box",
            ),
            Static("Pacotes extras (opcional — selecione com Enter):", classes="field-label"),
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
            selection_list = self.query_one("#extras-list", SelectionList)
            extras = list(selection_list.selected)

            self.app.config["hostname"] = hostname.value.strip() or "archlinux"
            self.app.config["packages"] = PACKAGES_BASE[:]
            self.app.config["extra_packages"] = extras
            self.go_next("bootloader")
        elif event.button.id == "btn-back":
            self.go_back("partition")
