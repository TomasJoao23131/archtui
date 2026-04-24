from textual.widgets import Static, Button, OptionList
from textual.containers import Horizontal
from installer.ui.sidebar import InstallerScreen


BOOTLOADERS = [
    ("GRUB (recomendado — funciona em UEFI e BIOS)", "grub"),
    ("systemd-boot (apenas UEFI — simples e leve)", "systemd-boot"),
    ("rEFInd (apenas UEFI — moderno com interface gráfica)", "refind"),
]


class BootloaderScreen(InstallerScreen):
    """Passo 5 — Escolha do bootloader."""

    STEP_NUMBER = 5
    STEP_NAME = "Bootloader"

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Passo 5 — Bootloader", id="header-text"),
            Static(
                "O bootloader é o programa que arranca o sistema operativo.\n"
                "Escolha o bootloader a instalar:\n\n"
                "• GRUB — O mais usado. Funciona em UEFI e BIOS legacy.\n"
                "  Recomendado se não tiver a certeza.\n\n"
                "• systemd-boot — Mais simples e rápido, mas só funciona\n"
                "  em sistemas UEFI.\n\n"
                "• rEFInd — Alternativa moderna com menu gráfico.\n"
                "  Também apenas para UEFI.",
                classes="help-text",
            ),
            OptionList(*[b[0] for b in BOOTLOADERS], id="bootloader-list"),
            Static(
                "ℹ  Se o seu sistema usa BIOS legacy (sem UEFI),\n"
                "   apenas o GRUB está disponível.",
                classes="info-text",
            ),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            option_list = self.query_one("#bootloader-list", OptionList)
            idx = option_list.highlighted if option_list.highlighted is not None else 0
            self.app.config["bootloader"] = BOOTLOADERS[idx][1]
            self.go_next("user")
        elif event.button.id == "btn-back":
            self.go_back("base")
