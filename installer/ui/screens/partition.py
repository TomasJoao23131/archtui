from textual.widgets import Static, Button, Input, OptionList
from textual.containers import Container, Horizontal
from installer.core import detect_disks
from installer.ui.sidebar import InstallerScreen


PARTITION_METHODS = [
    ("Particionamento Automatico (Apagar disco)", "auto"),
    ("Particionamento Manual (Avancado)", "manual"),
]


class PartitionScreen(InstallerScreen):
    STEP_NUMBER = 3
    STEP_NAME = "Particoes"

    def __init__(self):
        super().__init__()
        self._detected_disks = detect_disks()

    def compose(self):
        disk_options = [disk["label"] for disk in self._detected_disks] or ["Nenhum disco detectado"]
        content = Container(
            Static("Particionamento do Disco", id="header-text"),
            Static("Escolha o metodo de particionamento:", id="help-text"),
            OptionList(*[m[0] for m in PARTITION_METHODS], id="partition-list"),
            Static("Disco alvo para instalar:", id="disk-label"),
            OptionList(*disk_options, id="disk-list"),
            Static(
                "ATENCAO: O particionamento automatico ira apagar todo o disco!\n"
                "Escreva APAGAR para confirmar que aceita destruir o disco selecionado.\n"
                "Se precisar de dual boot ou particoes personalizadas, use o modo manual.",
                id="partition-help"
            ),
            Input(placeholder="APAGAR", id="confirm-erase-input"),
            Horizontal(
                Button("Anterior", id="btn-back", variant="default"),
                Button("Atualizar discos", id="btn-refresh", variant="default"),
                Button("Seguinte", id="btn-next", variant="primary"),
                id="nav-buttons"
            ),
            id="partition-container"
        )
        yield from self.compose_with_sidebar(content)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-refresh":
            self._detected_disks = detect_disks()
            self.app.action_switch_screen("partition")
            return

        if event.button.id == "btn-next":
            selected_index = self.get_highlighted_index("#partition-list")
            partition_method = PARTITION_METHODS[selected_index][1]
            if partition_method == "manual":
                self.notify("Modo manual ainda nao esta implementado.", severity="warning")
                return

            if not self._detected_disks:
                self.notify("Nenhum disco detectado no sistema.", severity="error")
                return

            disk_index = self.get_highlighted_index("#disk-list")
            if disk_index >= len(self._detected_disks):
                self.notify("Seleciona um disco valido.", severity="error")
                return

            confirm_input = self.query_one("#confirm-erase-input", Input)
            if confirm_input.value.strip().upper() != "APAGAR":
                self.notify("Escreve APAGAR para confirmar a destruicao do disco.", severity="error")
                return

            selected_disk = self._detected_disks[disk_index]
            self.app.config["partition_method"] = partition_method
            self.app.config["disk"] = selected_disk["path"]
            self.app.config["disk_label"] = selected_disk["label"]
            self.app.push_screen("base")
        elif event.button.id == "btn-back":
            self.app.pop_screen()
