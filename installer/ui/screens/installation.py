from threading import Thread
from textual.widgets import Static, Button, ProgressBar
from textual.binding import Binding
from textual.containers import Horizontal
from installer.core import ArchInstaller
from installer.ui.sidebar import InstallerScreen


class InstallationScreen(InstallerScreen):
    STEP_NUMBER = 9
    STEP_NAME = "Instalar"
    BINDINGS = [Binding("q", "quit", "Sair", show=False)]

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("A instalar...", id="header-text"),
            Static("Não desligue o computador. A aguardar...", classes="help-text"),
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
        self._last = 0
        self._done = False
        self._thread = Thread(target=self._installer.run, daemon=True)
        self._thread.start()
        self._timer = self.set_interval(0.5, self._tick)

    def _tick(self) -> None:
        p = self.query_one("#progress", ProgressBar)
        s = self.query_one("#status-text", Static)
        d = self.query_one("#detail-text", Static)
        l = self.query_one("#log-output", Static)
        p.update(progress=self._installer.progress)
        s.update(self._installer.status)
        d.update(f"Disco: {self.app.config.get('disk_label', '')}")
        if len(self._installer.logs) != self._last:
            self._last = len(self._installer.logs)
            l.update("\n".join(self._installer.logs[-12:]))
        if self._installer.finished:
            self.query_one("#btn-done", Button).label = "Concluído"
            self.query_one("#btn-done", Button).variant = "success"
            self._timer.stop()
            if not self._done:
                self._done = True
                sev = "information" if self._installer.success else "error"
                msg = "Instalação concluída!" if self._installer.success else (self._installer.error or "Erro")
                self.notify(msg, severity=sev)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-done":
            if hasattr(self, "_installer") and not self._installer.finished:
                self.notify("Não pode cancelar agora.", severity="warning")
                return
            self.app.exit()
