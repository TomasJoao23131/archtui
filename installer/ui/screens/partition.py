from textual.widgets import Static, Button, Input, OptionList
from textual.containers import Horizontal
from textual.binding import Binding
from installer.core import detect_disks
from installer.ui.sidebar import InstallerScreen


class PartitionScreen(InstallerScreen):
    """Passo 3 — Particionamento (requer confirmação, sem auto-avançar)."""

    STEP_NUMBER = 3
    STEP_NAME = "Partições"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def __init__(self):
        super().__init__()
        self._detected_disks = detect_disks()

    def compose(self):
        disk_options = (
            [d["label"] for d in self._detected_disks]
            if self._detected_disks
            else ["Nenhum disco detetado"]
        )

        yield from self.compose_with_sidebar(
            Static("Passo 3 — Particionamento do Disco", id="header-text"),
            Static(
                "O modo automático cria uma tabela GPT:\n"
                "  UEFI → EFI (512MB) + raiz  │  BIOS → boot (1MB) + raiz\n"
                "Selecione o disco e confirme com APAGAR.",
                classes="help-text",
            ),
            Static("Disco de destino:", classes="field-label"),
            OptionList(*disk_options, id="disk-list"),
            Static(
                "⚠  ATENÇÃO: APAGA TODO o disco selecionado!\n"
                "   Escreva APAGAR para confirmar:",
                classes="danger-text",
            ),
            Input(placeholder="Escreva APAGAR aqui", id="confirm-erase-input"),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("↻ Atualizar", id="btn-refresh", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-refresh":
            self._detected_disks = detect_disks()
            self.app.switch_screen("partition")
            return

        if event.button.id == "btn-next":
            self._try_advance()
        elif event.button.id == "btn-back":
            self.go_back("keyboard")

    def _try_advance(self) -> None:
        if not self._detected_disks:
            self.notify("Nenhum disco detetado.", severity="error")
            return

        disk_idx = self.get_highlighted("#disk-list")
        if disk_idx >= len(self._detected_disks):
            self.notify("Selecione um disco válido.", severity="error")
            return

        confirm = self.query_one("#confirm-erase-input", Input)
        if confirm.value.strip().upper() != "APAGAR":
            self.notify("Escreva APAGAR para confirmar.", severity="error")
            return

        disk = self._detected_disks[disk_idx]
        self.app.config["partition_method"] = "auto"
        self.app.config["disk"] = disk["path"]
        self.app.config["disk_label"] = disk["label"]
        self.go_next("base")

    def action_go_back(self) -> None:
        self.go_back("keyboard")
