from threading import Thread

from textual.widgets import Static, Button, ProgressBar
from textual.binding import Binding
from textual.containers import Horizontal
from installer.core import ArchInstaller
from installer.ui.sidebar import InstallerScreen


class InstallationScreen(InstallerScreen):
    """Passo 9 — Execução real da instalação."""

    STEP_NUMBER = 9
    STEP_NAME = "Instalação"

    BINDINGS = [Binding("q", "quit", "Sair")]

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Passo 9 — A Instalar o Arch Linux", id="header-text"),
            Static(
                "A instalação está em curso. Não desligue o computador.\n"
                "O progresso será atualizado automaticamente.",
                classes="help-text",
            ),
            ProgressBar(id="progress", total=100),
            Static("A preparar...", id="status-text"),
            Static("", id="detail-text"),
            Static("", id="log-output"),
            Horizontal(
                Button("A instalar...", id="btn-done", variant="error"),
                id="nav-buttons",
            ),
        )

    def on_mount(self) -> None:
        self._installer = ArchInstaller(dict(self.app.config))
        self._last_log_count = 0
        self._reported_finish = False
        self._install_thread = Thread(
            target=self._installer.run, daemon=True
        )
        self._install_thread.start()
        self._timer = self.set_interval(0.5, self._refresh)

    def _refresh(self) -> None:
        progress = self.query_one("#progress", ProgressBar)
        status = self.query_one("#status-text", Static)
        detail = self.query_one("#detail-text", Static)
        log_output = self.query_one("#log-output", Static)

        progress.update(progress=self._installer.progress)
        status.update(self._installer.status)

        disk_info = (
            self.app.config.get("disk_label")
            or self.app.config.get("disk", "")
        )
        detail.update(f"Disco: {disk_info}")

        if len(self._installer.logs) != self._last_log_count:
            self._last_log_count = len(self._installer.logs)
            recent = self._installer.logs[-14:]
            log_output.update("\n".join(recent))

        if self._installer.finished:
            btn = self.query_one("#btn-done", Button)
            btn.label = "Concluído — Fechar"
            btn.variant = "success"
            self._timer.stop()
            if not self._reported_finish:
                self._reported_finish = True
                if self._installer.success:
                    self.notify(
                        "Instalação concluída com sucesso!",
                        severity="information",
                    )
                else:
                    self.notify(
                        self._installer.error or "Erro na instalação.",
                        severity="error",
                    )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-done":
            if hasattr(self, "_installer") and not self._installer.finished:
                self.notify(
                    "Não é possível cancelar durante a instalação.",
                    severity="warning",
                )
                return
            if hasattr(self, "_timer"):
                self._timer.stop()
            self.app.exit()
