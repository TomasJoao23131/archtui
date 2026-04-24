from textual.widgets import Static, Button, Input, OptionList
from textual.containers import Horizontal
from installer.core import detect_disks
from installer.ui.sidebar import InstallerScreen


PARTITION_METHODS = [
    ("Automático (apaga todo o disco)", "auto"),
]


class PartitionScreen(InstallerScreen):
    """Passo 3 — Particionamento do disco."""

    STEP_NUMBER = 3
    STEP_NAME = "Partições"

    def __init__(self):
        super().__init__()
        self._detected_disks = detect_disks()

    def compose(self):
        disk_options = (
            [disk["label"] for disk in self._detected_disks]
            if self._detected_disks
            else ["Nenhum disco detetado"]
        )

        yield from self.compose_with_sidebar(
            Static("Passo 3 — Particionamento do Disco", id="header-text"),
            Static(
                "Escolha como particionar o disco de destino.\n"
                "De momento, apenas o modo automático está disponível.\n"
                "O modo automático cria uma tabela GPT com:\n"
                "  • UEFI: partição EFI (512 MB) + partição raiz\n"
                "  • BIOS: partição BIOS boot (1 MB) + partição raiz",
                classes="help-text",
            ),
            Static("Método de particionamento:", classes="field-label"),
            OptionList(*[m[0] for m in PARTITION_METHODS], id="partition-list"),
            Static("Disco de destino:", classes="field-label"),
            OptionList(*disk_options, id="disk-list"),
            Static(
                "⚠  ATENÇÃO: O particionamento automático APAGA TODO o disco!\n"
                "   Todos os dados serão perdidos permanentemente.\n"
                "   Escreva APAGAR abaixo para confirmar.",
                classes="danger-text",
            ),
            Input(placeholder="Escreva APAGAR para confirmar", id="confirm-erase-input"),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("Atualizar discos", id="btn-refresh", variant="default"),
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
            # Validar método
            option_list = self.query_one("#partition-list", OptionList)
            idx = option_list.highlighted if option_list.highlighted is not None else 0
            partition_method = PARTITION_METHODS[idx][1]

            # Validar disco
            if not self._detected_disks:
                self.notify("Nenhum disco detetado. Verifique a ligação.", severity="error")
                return

            disk_list = self.query_one("#disk-list", OptionList)
            disk_idx = disk_list.highlighted if disk_list.highlighted is not None else 0
            if disk_idx >= len(self._detected_disks):
                self.notify("Selecione um disco válido.", severity="error")
                return

            # Validar confirmação
            confirm_input = self.query_one("#confirm-erase-input", Input)
            if confirm_input.value.strip().upper() != "APAGAR":
                self.notify(
                    "Escreva APAGAR para confirmar a destruição do disco.",
                    severity="error",
                )
                return

            selected_disk = self._detected_disks[disk_idx]
            self.app.config["partition_method"] = partition_method
            self.app.config["disk"] = selected_disk["path"]
            self.app.config["disk_label"] = selected_disk["label"]
            self.go_next("base")

        elif event.button.id == "btn-back":
            self.go_back("keyboard")
