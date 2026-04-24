from textual.widgets import Static, Button, OptionList, Switch
from textual.containers import Horizontal
from textual.binding import Binding
from installer.ui.sidebar import InstallerScreen


DESKTOPS = [
    ("GNOME  (completo, moderno)", "gnome"),
    ("KDE Plasma  (personalizável)", "kde"),
    ("XFCE  (leve, PCs antigos)", "xfce"),
    ("MATE  (clássico)", "mate"),
    ("Cinnamon  (estilo Windows)", "cinnamon"),
    ("Apenas CLI  (sem gráficos)", "cli"),
]

VIDEO_DRIVERS = [
    ("Auto  (genérico)", "auto"),
    ("Intel  (integrada)", "intel"),
    ("AMD  (Radeon)", "amd"),
    ("NVIDIA  (proprietário)", "nvidia"),
    ("VM  (VMware/VBox)", "vm"),
]


class DesktopScreen(InstallerScreen):
    """Passo 7 — Ambiente + drivers."""

    STEP_NUMBER = 7
    STEP_NAME = "Ambiente"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Passo 7 — Ambiente de Trabalho", id="header-text"),
            Static(
                "Escolha o ambiente gráfico e driver de vídeo.\n"
                "Tab para mudar entre listas. Enter/botão para avançar.",
                classes="help-text",
            ),
            Static("Ambiente:", classes="field-label"),
            OptionList(*[d[0] for d in DESKTOPS], id="desktop-list"),
            Static("Driver de vídeo:", classes="field-label"),
            OptionList(*[d[0] for d in VIDEO_DRIVERS], id="video-driver-list"),
            Horizontal(
                Switch(True, id="multilib-switch"),
                Static("  Multilib (32-bit, jogos/Wine)", classes="field-label"),
                classes="switch-row",
            ),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            d = self.get_highlighted("#desktop-list")
            v = self.get_highlighted("#video-driver-list")
            m = self.query_one("#multilib-switch", Switch).value
            self.app.config["desktop"] = DESKTOPS[d][1]
            self.app.config["video_driver"] = VIDEO_DRIVERS[v][1]
            self.app.config["multilib"] = m
            self.go_next("summary")
        elif event.button.id == "btn-back":
            self.go_back("user")

    def action_go_back(self) -> None:
        self.go_back("user")
