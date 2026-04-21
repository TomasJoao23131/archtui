from textual.widgets import Static, Button, OptionList, Switch
from textual.containers import Container, Horizontal
from installer.ui.sidebar import InstallerScreen


DESKTOPS = [
    ("GNOME (Ambiente completo)", "gnome"),
    ("KDE Plasma (KDE5)", "kde"),
    ("XFCE (Leve)", "xfce"),
    ("MATE (Classico)", "mate"),
    ("Cinnamon", "cinnamon"),
    ("Apenas CLI (Sem ambiente grafico)", "cli"),
]

VIDEO_DRIVERS = [
    ("Automatico (detectado)", "auto"),
    ("Intel (i915)", "intel"),
    ("AMD (amdgpu)", "amd"),
    ("NVIDIA (proprietario)", "nvidia"),
    ("VMware / VirtualBox", "vm"),
]


class DesktopScreen(InstallerScreen):
    STEP_NUMBER = 7
    STEP_NAME = "Ambiente"

    def compose(self):
        content = Container(
            Static("Selecionar Ambiente de Trabalho", id="header-text"),
            OptionList(*[d[0] for d in DESKTOPS], id="desktop-list"),
            Static("Drivers de video:", id="video-label"),
            OptionList(*[driver[0] for driver in VIDEO_DRIVERS], id="video-driver-list"),
            Switch(True, id="multilib-switch"),
            Static("Habilitar repositorio multilib (32-bit)", id="multilib-label"),
            Horizontal(
                Button("Anterior", id="btn-back", variant="default"),
                Button("Seguinte", id="btn-next", variant="primary"),
                id="nav-buttons"
            ),
            id="desktop-container"
        )
        yield from self.compose_with_sidebar(content)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            desktop_index = self.get_highlighted_index("#desktop-list")
            driver_index = self.get_highlighted_index("#video-driver-list")
            multilib_switch = self.query_one("#multilib-switch", Switch)
            self.app.config["desktop"] = DESKTOPS[desktop_index][1]
            self.app.config["video_driver"] = VIDEO_DRIVERS[driver_index][1]
            self.app.config["multilib"] = multilib_switch.value
            self.app.push_screen("summary")
        elif event.button.id == "btn-back":
            self.app.pop_screen()
