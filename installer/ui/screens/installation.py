from threading import Thread

from textual.widgets import Static, Button, ProgressBar
from textual.binding import Binding
from textual.containers import Container, Horizontal
from installer.core import ArchInstaller
from installer.ui.sidebar import InstallerScreen


class InstallationScreen(InstallerScreen):
    STEP_NUMBER = 9
    STEP_NAME = "Instalacao"

    BINDINGS = [
        Binding("q", "quit", "Sair"),
    ]

    def compose(self):
        content = Container(
            Static("A Instalar o Arch Linux...", id="header-text"),
            ProgressBar(id="progress", total=100),
            Static("A preparar instalacao real...", id="status-text"),
            Static(
                "A instalacao automatica vai apagar o disco escolhido e executar os comandos reais do Arch.",
                id="detail-text",
            ),
            Static("", id="log-output"),
            Horizontal(
                Button("A instalar...", id="btn-cancel", variant="error"),
                id="nav-buttons"
            ),
            id="install-container"
        )
        yield from self.compose_with_sidebar(content)

    def on_mount(self) -> None:
        self._installer = ArchInstaller(dict(self.app.config))
        self._last_log_count = 0
        self._reported_finish = False
        self._install_thread = Thread(target=self._installer.run, daemon=True)
        self._install_thread.start()
        self._install_timer = self.set_interval(0.5, self.refresh_installation)

    def refresh_installation(self) -> None:
        progress = self.query_one("#progress", ProgressBar)
        status = self.query_one("#status-text", Static)
        detail = self.query_one("#detail-text", Static)
        log_output = self.query_one("#log-output", Static)

        progress.update(progress=self._installer.progress)
        status.update(self._installer.status)
        detail.update(
            f"Disco alvo: {self.app.config.get('disk_label') or self.app.config.get('disk', 'indefinido')}"
        )

        if len(self._installer.logs) != self._last_log_count:
            self._last_log_count = len(self._installer.logs)
            recent_logs = self._installer.logs[-14:]
            log_output.update("\n".join(recent_logs))

        if self._installer.finished:
            self.query_one("#btn-cancel", Button).label = "Voltar"
            self._install_timer.stop()
            if not self._reported_finish:
                self._reported_finish = True
                if self._installer.success:
                    self.notify("Instalacao concluida com sucesso.", severity="information")
                else:
                    self.notify(self._installer.error or "Falha na instalacao.", severity="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-cancel":
            if hasattr(self, "_installer") and not self._installer.finished:
                self.notify("Cancelar durante a instalacao nao e suportado com seguranca.", severity="warning")
                return
            if hasattr(self, "_install_timer"):
                self._install_timer.stop()
            self.app.pop_screen()
