from textual.widgets import Static, Button
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from installer.ui.sidebar import InstallerScreen


class SummaryScreen(InstallerScreen):
    STEP_NUMBER = 8
    STEP_NAME = "Resumo"

    BINDINGS = [
        Binding("q", "quit", "Sair"),
    ]

    def compose(self):
        lang_display = self.app.config.get("language", "pt_BR")
        kb_display = self.app.config.get("keyboard", "br-abnt2")
        disk_display = self.app.config.get("disk_label") or self.app.config.get("disk", "/dev/sda")
        hostname_display = self.app.config.get("hostname", "archlinux")
        user_display = self.app.config.get("username", "usuario")
        desktop_display = self.app.config.get("desktop", "gnome")
        bootloader_display = self.app.config.get("bootloader", "grub")
        driver_display = self.app.config.get("video_driver", "auto")
        extras_display = self.app.config.get("extra_packages", [])
        multilib_display = "sim" if self.app.config.get("multilib", True) else "nao"
        extras_text = ", ".join(extras_display) if extras_display else "nenhum"

        summary_text = (
            f"Resumo da Instalacao\n"
            f"=====================\n\n"
            f"Idioma: {lang_display}\n"
            f"Teclado: {kb_display}\n"
            f"Disco: {disk_display}\n"
            f"Hostname: {hostname_display}\n"
            f"Utilizador: {user_display}\n"
            f"Ambiente: {desktop_display}\n"
            f"Driver de video: {driver_display}\n"
            f"Multilib: {multilib_display}\n"
            f"Extras: {extras_text}\n"
            f"Bootloader: {bootloader_display}\n\n"
            f"Clique em 'Instalar' para iniciar a instalacao.\n"
            f"O modo automatico APAGA totalmente o disco selecionado.\n"
            f"Certifique-se de que tem uma copia de seguranca dos seus dados."
        )

        content = Container(
            Static("Resumo da Configuracao", id="header-text"),
            Vertical(
                Static(summary_text, id="summary-content"),
                id="summary-inner"
            ),
            Horizontal(
                Button("Anterior", id="btn-back", variant="default"),
                Button("Instalar!", id="btn-install", variant="success"),
                id="nav-buttons"
            ),
            id="summary-container"
        )
        yield from self.compose_with_sidebar(content)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.app.pop_screen()
        elif event.button.id == "btn-install":
            if not self.app.config.get("disk"):
                self.notify("Seleciona um disco antes de instalar.", severity="error")
                return
            self.app.push_screen("installation")
