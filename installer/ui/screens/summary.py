from textual.widgets import Static, Button
from textual.binding import Binding
from textual.containers import Container, Horizontal
from installer.ui.sidebar import InstallerScreen


class SummaryScreen(InstallerScreen):
    """Passo 8 — Resumo de tudo antes de instalar."""

    STEP_NUMBER = 8
    STEP_NAME = "Resumo"

    BINDINGS = [Binding("q", "quit", "Sair")]

    def compose(self):
        c = self.app.config
        lang = c.get("language", "pt_BR")
        kb = c.get("keyboard", "br-abnt2")
        disk = c.get("disk_label") or c.get("disk", "(nenhum)")
        hostname = c.get("hostname", "archlinux")
        username = c.get("username", "(não definido)")
        desktop = c.get("desktop", "gnome")
        bootloader = c.get("bootloader", "grub")
        video = c.get("video_driver", "auto")
        extras = c.get("extra_packages", [])
        multilib = "Sim" if c.get("multilib", True) else "Não"
        sudo = "Sim" if c.get("sudo", False) else "Não"
        extras_text = ", ".join(extras) if extras else "nenhum"

        summary = (
            f"  Idioma:           {lang}\n"
            f"  Teclado:          {kb}\n"
            f"  Disco:            {disk}\n"
            f"  Hostname:         {hostname}\n"
            f"  Utilizador:       {username}\n"
            f"  Sudo:             {sudo}\n"
            f"  Ambiente:         {desktop}\n"
            f"  Driver de vídeo:  {video}\n"
            f"  Multilib:         {multilib}\n"
            f"  Extras:           {extras_text}\n"
            f"  Bootloader:       {bootloader}"
        )

        yield from self.compose_with_sidebar(
            Static("Passo 8 — Resumo", id="header-text"),
            Static(
                "Reveja todas as configurações antes de instalar.\n"
                "Pode voltar atrás para alterar qualquer opção.",
                classes="help-text",
            ),
            Container(
                Static(summary, id="summary-content"),
                id="summary-box",
            ),
            Static(
                "⚠  Ao clicar 'Instalar', o disco será APAGADO.\n"
                "   Esta ação é IRREVERSÍVEL.",
                classes="danger-text",
            ),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("✓ Instalar!", id="btn-install", variant="success"),
                id="nav-buttons",
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.go_back("desktop")
        elif event.button.id == "btn-install":
            if not self.app.config.get("disk"):
                self.notify("Nenhum disco selecionado.", severity="error")
                return
            self.go_next("installation")
