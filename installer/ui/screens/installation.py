import subprocess
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
            Static("Nao desligue o computador. A aguardar...", classes="help-text"),
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
        self._reboot_countdown = -1
        self._thread = Thread(target=self._installer.run, daemon=True)
        self._thread.start()
        self._timer = self.set_interval(0.5, self._tick)

    def _tick(self) -> None:
        p = self.query_one("#progress", ProgressBar)
        s = self.query_one("#status-text", Static)
        d = self.query_one("#detail-text", Static)
        log = self.query_one("#log-output", Static)
        p.update(progress=self._installer.progress)
        s.update(self._installer.status)
        d.update(f"Disco: {self.app.config.get('disk_label', '')}")
        if len(self._installer.logs) != self._last:
            self._last = len(self._installer.logs)
            log.update("\n".join(self._installer.logs[-12:]))
        if self._installer.finished and not self._done:
            self._done = True
            btn = self.query_one("#btn-done", Button)
            if self._installer.success:
                btn.label = "Reiniciar Agora"
                btn.variant = "success"
                sev = "information"
                msg = "Instalacao concluida! A reiniciar em 10s..."
                # Iniciar countdown para reboot automatico
                self._reboot_countdown = 20  # 20 ticks de 0.5s = 10 segundos
            else:
                btn.label = "Fechar"
                btn.variant = "error"
                sev = "error"
                msg = self._installer.error or "Erro na instalacao"
            self.notify(msg, severity=sev)
        # Countdown para reboot automatico
        if self._reboot_countdown > 0:
            self._reboot_countdown -= 1
            seconds = self._reboot_countdown // 2
            btn = self.query_one("#btn-done", Button)
            btn.label = f"Reiniciar Agora ({seconds}s)"
        elif self._reboot_countdown == 0:
            self._reboot_countdown = -1
            self._timer.stop()
            self._do_reboot()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-done":
            if hasattr(self, "_installer") and not self._installer.finished:
                self.notify("Nao pode cancelar agora.", severity="warning")
                return
            if self._installer.success:
                self._do_reboot()
            else:
                self.app.exit()

    def _do_reboot(self) -> None:
        self.app.exit()
        try:
            subprocess.run(["reboot"], check=False)
        except Exception:
            pass
