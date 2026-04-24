from textual.widgets import Static, Button, RadioSet, RadioButton
from textual.containers import Horizontal
from textual.binding import Binding
from installer.ui.sidebar import InstallerScreen


BOOTLOADERS = [
    ("GRUB (recomendado, funciona em UEFI e BIOS)", "grub"),
    ("systemd-boot (apenas UEFI, muito leve)", "systemd-boot"),
    ("rEFInd (apenas UEFI, menu gráfico)", "refind"),
]


class BootloaderScreen(InstallerScreen):
    STEP_NUMBER = 5
    STEP_NAME = "Bootloader"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Bootloader", id="header-text"),
            Static(
                "O bootloader é o programa que arranca o sistema operativo.\n"
                "Se não tiveres a certeza, o GRUB é a opção mais segura e compatível.",
                classes="help-text",
            ),
            RadioSet(
                *[RadioButton(b[0], id=f"boot-{i}") for i, b in enumerate(BOOTLOADERS)],
                id="bootloader-list",
            ),
            Static(
                "NOTA\n"
                "Se o teu sistema for BIOS legacy (computador antigo), apenas o GRUB\n"
                "irá funcionar corretamente.",
                classes="note-box",
            ),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_mount(self):
        self.query_one("#boot-0", RadioButton).value = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            idx = self.get_radio_index("#bootloader-list")
            self.app.config["bootloader"] = BOOTLOADERS[idx][1]
            self.go_next("user")
        elif event.button.id == "btn-back":
            self.go_back("base")

    def action_go_back(self) -> None:
        self.go_back("base")
