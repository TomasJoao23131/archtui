from textual.widgets import Static, Button, OptionList
from textual.containers import Container, Horizontal
from installer.ui.sidebar import InstallerScreen


BOOTLOADERS = [
    ("GRUB (Recomendado)", "grub"),
    ("systemd-boot", "systemd-boot"),
    ("rEFInd", "refind"),
]


class BootloaderScreen(InstallerScreen):
    STEP_NUMBER = 5
    STEP_NAME = "Bootloader"

    def compose(self):
        content = Container(
            Static("Selecionar Bootloader", id="header-text"),
            OptionList(*[b[0] for b in BOOTLOADERS], id="bootloader-list"),
            Static(
                "GRUB e o bootloader mais utilizado e recomendado para a maioria\n"
                "dos utilizadores. systemd-boot e mais simples e leve.\n"
                "rEFInd e uma alternativa moderna com suporte UEFI.",
                id="bootloader-help"
            ),
            Horizontal(
                Button("Anterior", id="btn-back", variant="default"),
                Button("Seguinte", id="btn-next", variant="primary"),
                id="nav-buttons"
            ),
            id="bootloader-container"
        )
        yield from self.compose_with_sidebar(content)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            selected_index = self.get_highlighted_index("#bootloader-list")
            self.app.config["bootloader"] = BOOTLOADERS[selected_index][1]
            self.app.push_screen("user")
        elif event.button.id == "btn-back":
            self.app.pop_screen()
