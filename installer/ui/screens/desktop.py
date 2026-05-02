from textual.widgets import Static, Button, RadioSet, RadioButton, Checkbox
from textual.containers import Horizontal
from textual.binding import Binding
from installer.ui.sidebar import InstallerScreen


DESKTOPS = [
    ("GNOME (completo e moderno)", "gnome"),
    ("KDE Plasma (altamente personalizável)", "kde"),
    ("XFCE (leve e rápido, ideal para PCs mais antigos)", "xfce"),
    ("MATE (clássico e estável)", "mate"),
    ("Cinnamon (familiar, estilo Windows)", "cinnamon"),
    ("Budgie (elegante e simples)", "budgie"),
    ("LXQt (ultra-leve, para hardware limitado)", "lxqt"),
    ("Deepin (visual polido, inspirado em macOS)", "deepin"),
    ("i3 (tiling window manager para utilizadores avançados)", "i3"),
    ("Sway (tiling WM para Wayland, alternativa ao i3)", "sway"),
    ("Hyprland (tiling WM Wayland com animações)", "hyprland"),
    ("Apenas CLI (linha de comandos, sem gráficos)", "cli"),
]

VIDEO_DRIVERS = [
    ("Automático (deteta o hardware)", "auto"),
    ("Intel (gráficos integrados)", "intel"),
    ("AMD (Radeon)", "amd"),
    ("NVIDIA (driver proprietário)", "nvidia"),
    ("Nouveau (NVIDIA open-source)", "nouveau"),
    ("VMware / VirtualBox (máquina virtual)", "vm"),
]


class DesktopScreen(InstallerScreen):
    STEP_NUMBER = 7
    STEP_NAME = "Desktop"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Ambiente de Trabalho", id="header-text"),
            Static("Escolhe o ambiente gráfico e os drivers de vídeo.", classes="help-text"),
            Static("Ambiente:", classes="field-label"),
            RadioSet(
                *[RadioButton(d[0], id=f"desk-{i}") for i, d in enumerate(DESKTOPS)],
                id="desktop-list",
            ),
            Checkbox("Usar Ecrã de Login Gráfico (SDDM/LightDM) para i3, Sway ou Hyprland", id="dm-checkbox", value=True),
            Static("Driver de vídeo:", classes="field-label"),
            RadioSet(
                *[RadioButton(v[0], id=f"vid-{i}") for i, v in enumerate(VIDEO_DRIVERS)],
                id="video-driver-list",
            ),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_mount(self):
        self.query_one("#desk-0", RadioButton).value = True
        self.query_one("#vid-0", RadioButton).value = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            d_idx = self.get_radio_index("#desktop-list")
            v_idx = self.get_radio_index("#video-driver-list")
            try:
                use_dm = self.query_one("#dm-checkbox", Checkbox).value
            except Exception:
                use_dm = False
            self.app.config["desktop"] = DESKTOPS[d_idx][1]
            self.app.config["video_driver"] = VIDEO_DRIVERS[v_idx][1]
            self.app.config["use_dm"] = use_dm
            self.go_next("summary")
        elif event.button.id == "btn-back":
            self.go_back("user")

    def action_go_back(self) -> None:
        self.go_back("user")
