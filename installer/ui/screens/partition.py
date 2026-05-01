from textual.widgets import Static, Button, Input, RadioSet, RadioButton, Switch
from textual.containers import Horizontal
from textual.binding import Binding
from installer.core import detect_disks
from installer.ui.sidebar import InstallerScreen

SWAP_SIZES = [
    ("2 GB (recomendado para 4-8 GB RAM)", "2G"),
    ("4 GB (recomendado para 8-16 GB RAM)", "4G"),
    ("8 GB (para hibernacao com 8+ GB RAM)", "8G"),
    ("Sem swap", "none"),
]


class PartitionScreen(InstallerScreen):
    STEP_NUMBER = 3
    STEP_NAME = "Particoes"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def __init__(self):
        super().__init__()
        self._detected_disks = detect_disks()

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Esquema de particoes", id="header-text"),
            Static(
                "Escolhe como queres organizar o disco. O modo automatico\n"
                "cria uma tabela GPT com UEFI ou BIOS boot e particao raiz.",
                classes="help-text",
            ),
            RadioSet(
                RadioButton("Automatico (recomendado) - Apaga o disco", id="part-0", value=True),
                id="partition-list",
            ),
            Static("Disco de destino:", classes="field-label"),
            self._build_disk_radios(),
            Static("Swap (memoria virtual):", classes="field-label"),
            RadioSet(
                *[RadioButton(s[0], id=f"swap-{i}") for i, s in enumerate(SWAP_SIZES)],
                id="swap-list",
            ),
            Static(
                "NOTA\n"
                "O particionamento automatico APAGA TODO o disco selecionado.\n"
                "Escreve APAGAR na caixa abaixo para confirmar a destruicao dos dados.",
                classes="note-box",
            ),
            Input(placeholder="Escreve APAGAR para confirmar...", id="confirm-erase-input"),
            Horizontal(
                Button("<- Anterior", id="btn-back", variant="default"),
                Button("Atualizar Discos", id="btn-refresh", variant="default"),
                Button("Seguinte ->", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def _build_disk_radios(self):
        radios = []
        if self._detected_disks:
            for i, d in enumerate(self._detected_disks):
                radios.append(RadioButton(d["label"], id=f"disk-{i}"))
        else:
            radios.append(RadioButton("Nenhum disco detetado", id="disk-0", disabled=True))

        rs = RadioSet(*radios, id="disk-list")
        return rs

    def on_mount(self):
        if self._detected_disks:
            try:
                self.query_one("#disk-0", RadioButton).value = True
            except Exception:
                pass
        self.query_one("#swap-0", RadioButton).value = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-refresh":
            self._detected_disks = detect_disks()
            self.recompose()
            return

        if event.button.id == "btn-next":
            self._try_advance()
        elif event.button.id == "btn-back":
            self.go_back("keyboard")

    def _try_advance(self) -> None:
        if not self._detected_disks:
            self.notify("Nenhum disco detetado.", severity="error")
            return

        disk_idx = self.get_radio_index("#disk-list")
        if disk_idx >= len(self._detected_disks):
            self.notify("Selecione um disco valido.", severity="error")
            return

        confirm = self.query_one("#confirm-erase-input", Input)
        if confirm.value.strip().upper() != "APAGAR":
            self.notify("Escreve APAGAR para confirmar.", severity="error")
            return

        swap_idx = self.get_radio_index("#swap-list")
        swap_size = SWAP_SIZES[swap_idx][1]

        disk = self._detected_disks[disk_idx]
        self.app.config["partition_method"] = "auto"
        self.app.config["disk"] = disk["path"]
        self.app.config["disk_label"] = disk["label"]
        self.app.config["swap_size"] = swap_size
        self.go_next("base")

    def action_go_back(self) -> None:
        self.go_back("keyboard")
