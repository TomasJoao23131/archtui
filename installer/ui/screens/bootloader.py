from textual.widgets import Static, Button, OptionList
from textual.containers import Horizontal
from textual.binding import Binding
from installer.ui.sidebar import InstallerScreen


BOOTLOADERS = [
    ("GRUB  (recomendado, UEFI + BIOS)", "grub"),
    ("systemd-boot  (apenas UEFI, leve)", "systemd-boot"),
    ("rEFInd  (apenas UEFI, moderno)", "refind"),
]


class BootloaderScreen(InstallerScreen):
    """Passo 5 — Enter na lista avança."""

    STEP_NUMBER = 5
    STEP_NAME = "Bootloader"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Passo 5 — Bootloader", id="header-text"),
            Static(
                "O bootloader arranca o sistema operativo.\n"
                "Use ↑↓ para escolher e Enter para confirmar.\n\n"
                "• GRUB — Funciona em tudo. Escolha este se tiver dúvidas.\n"
                "• systemd-boot — Simples e rápido, só UEFI.\n"
                "• rEFInd — Menu gráfico moderno, só UEFI.",
                classes="help-text",
            ),
            OptionList(*[b[0] for b in BOOTLOADERS], id="bootloader-list"),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_list.id == "bootloader-list":
            self.app.config["bootloader"] = BOOTLOADERS[event.option_index][1]
            self.go_next("user")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            idx = self.get_highlighted("#bootloader-list")
            self.app.config["bootloader"] = BOOTLOADERS[idx][1]
            self.go_next("user")
        elif event.button.id == "btn-back":
            self.go_back("base")

    def action_go_back(self) -> None:
        self.go_back("base")
