from textual.widgets import Static, Button, Input, SelectionList, RadioSet, RadioButton
from textual.containers import Container, Horizontal
from textual.binding import Binding
from installer.ui.sidebar import InstallerScreen


KERNELS = [
    (
        "linux (padrao, ultimas novidades)",
        "linux",
        "O kernel padrao do Arch. Recebe as atualizacoes mais recentes\n"
        "e suporta o hardware mais novo. Recomendado para a maioria.",
    ),
    (
        "linux-lts (longa duracao, maximo de estabilidade)",
        "linux-lts",
        "Kernel com suporte de longa duracao. Recebe menos atualizacoes\n"
        "mas e mais estavel. Ideal para servidores ou PCs de trabalho.",
    ),
    (
        "linux-zen (otimizado para desktop e jogos)",
        "linux-zen",
        "Kernel otimizado para uso interativo. Melhor resposta em jogos,\n"
        "audio e multitarefa. Ideal para gaming e uso diario intenso.",
    ),
]

PACKAGES_BASE = [
    "base", "base-devel", "linux-firmware",
    "vim", "nano", "openssh", "networkmanager", "sudo",
]

PACKAGES_EXTRAS = [
    ("Firefox (navegador)", "firefox"),
    ("LibreOffice (escritorio)", "libreoffice-fresh"),
    ("Git (controlo de versoes)", "git"),
    ("htop (monitor de processos)", "htop"),
    ("neofetch (info do sistema)", "neofetch"),
    ("wget + curl (downloads)", "wget curl"),
    ("unzip + p7zip (descompressao)", "unzip p7zip"),
    ("Servidor Xorg (necessario para WMs X11)", "xorg-server"),
    ("PipeWire (audio moderno)", "pipewire pipewire-pulse wireplumber"),
    ("Bluetooth (bluez)", "bluez bluez-utils"),
    ("Impressoras (CUPS)", "cups cups-pdf"),
    ("NetworkManager applet (tray icon WiFi)", "network-manager-applet"),
    ("Flatpak (apps universais)", "flatpak"),
    ("NTFS suporte (ler discos Windows)", "ntfs-3g"),
]


class BaseSystemScreen(InstallerScreen):
    STEP_NUMBER = 4
    STEP_NAME = "Sistema base"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Sistema Base", id="header-text"),
            Static(
                "Define o kernel, hostname e pacotes adicionais do teu sistema.",
                classes="help-text",
            ),
            Static("Kernel Linux:", classes="field-label"),
            RadioSet(
                *[RadioButton(k[0], id=f"kernel-{i}") for i, k in enumerate(KERNELS)],
                id="kernel-list",
            ),
            Static(KERNELS[0][2], id="kernel-desc", classes="info-text"),
            Static("Hostname (nome do pc na rede):", classes="field-label"),
            Input(placeholder="archlinux", id="hostname-input", value="archlinux"),
            Static("Pacotes adicionais (opcional, usa [Espaco] para marcar):", classes="field-label"),
            SelectionList(*PACKAGES_EXTRAS, id="extras-list"),
            Horizontal(
                Button("<- Anterior", id="btn-back", variant="default"),
                Button("Seguinte ->", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_mount(self):
        self.query_one("#kernel-0", RadioButton).value = True

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        if event.radio_set.id == "kernel-list":
            idx = event.radio_set.pressed_index
            if 0 <= idx < len(KERNELS):
                try:
                    desc = self.query_one("#kernel-desc", Static)
                    desc.update(KERNELS[idx][2])
                except Exception:
                    pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            hostname = self.query_one("#hostname-input", Input)
            extras = self.get_selected_values("#extras-list")
            kernel_idx = self.get_radio_index("#kernel-list")
            kernel = KERNELS[kernel_idx][1]

            # Construir lista de pacotes base com o kernel escolhido
            packages = PACKAGES_BASE[:]
            packages.append(kernel)
            # Adicionar headers para compilacao de modulos (dkms, nvidia, etc.)
            packages.append(f"{kernel}-headers")

            self.app.config["hostname"] = hostname.value.strip() or "archlinux"
            self.app.config["kernel"] = kernel
            self.app.config["packages"] = packages
            self.app.config["extra_packages"] = extras
            self.go_next("bootloader")
        elif event.button.id == "btn-back":
            self.go_back("partition")

    def action_go_back(self) -> None:
        self.go_back("partition")
