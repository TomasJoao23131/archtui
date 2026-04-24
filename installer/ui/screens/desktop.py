from textual.widgets import Static, Button, OptionList, Switch
from textual.containers import Horizontal
from installer.ui.sidebar import InstallerScreen


DESKTOPS = [
    ("GNOME (completo, moderno, muito usado)", "gnome"),
    ("KDE Plasma (personalizável, visual elegante)", "kde"),
    ("XFCE (leve e estável, bom para PCs antigos)", "xfce"),
    ("MATE (clássico, baseado no GNOME 2)", "mate"),
    ("Cinnamon (familiar, estilo Windows)", "cinnamon"),
    ("Apenas CLI (sem interface gráfica)", "cli"),
]

VIDEO_DRIVERS = [
    ("Automático (deteção genérica)", "auto"),
    ("Intel (placas integradas Intel)", "intel"),
    ("AMD (Radeon / integradas AMD)", "amd"),
    ("NVIDIA (driver proprietário)", "nvidia"),
    ("VMware / VirtualBox (máquina virtual)", "vm"),
]


class DesktopScreen(InstallerScreen):
    """Passo 7 — Ambiente de trabalho e drivers de vídeo."""

    STEP_NUMBER = 7
    STEP_NAME = "Ambiente"

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Passo 7 — Ambiente de Trabalho", id="header-text"),
            Static(
                "Escolha o ambiente gráfico a instalar.\n"
                "Se não tiver a certeza, GNOME ou KDE Plasma são boas opções.\n"
                "Escolha 'Apenas CLI' se quiser um servidor sem interface gráfica.",
                classes="help-text",
            ),
            Static("Ambiente de trabalho:", classes="field-label"),
            OptionList(*[d[0] for d in DESKTOPS], id="desktop-list"),
            Static("Driver de vídeo:", classes="field-label"),
            OptionList(*[d[0] for d in VIDEO_DRIVERS], id="video-driver-list"),
            Horizontal(
                Switch(True, id="multilib-switch"),
                Static(
                    "  Ativar repositório multilib (pacotes 32-bit, necessário para jogos/Wine)",
                    classes="field-label",
                ),
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
            desktop_list = self.query_one("#desktop-list", OptionList)
            driver_list = self.query_one("#video-driver-list", OptionList)
            multilib_switch = self.query_one("#multilib-switch", Switch)

            d_idx = desktop_list.highlighted if desktop_list.highlighted is not None else 0
            v_idx = driver_list.highlighted if driver_list.highlighted is not None else 0

            self.app.config["desktop"] = DESKTOPS[d_idx][1]
            self.app.config["video_driver"] = VIDEO_DRIVERS[v_idx][1]
            self.app.config["multilib"] = multilib_switch.value
            self.go_next("summary")
        elif event.button.id == "btn-back":
            self.go_back("user")
