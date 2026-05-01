from textual.widgets import Static, Button
from textual.binding import Binding
from textual.containers import Container, Horizontal
from installer.ui.sidebar import InstallerScreen


class SummaryScreen(InstallerScreen):
    STEP_NUMBER = 8
    STEP_NAME = "Confirmar"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def compose(self):
        c = self.app.config
        swap = c.get("swap_size", "2G")
        swap_label = "Desativado" if swap == "none" else swap

        lines = [
            f"  Idioma:          {c.get('language', 'pt_BR')}",
            f"  Fuso horario:    {c.get('timezone', 'UTC')}",
            f"  Teclado:         {c.get('keyboard', 'br-abnt2')}",
            f"  Disco:           {c.get('disk_label') or c.get('disk', '---')}",
            f"  Swap:            {swap_label}",
            f"  Kernel:          {c.get('kernel', 'linux')}",
            f"  Hostname:        {c.get('hostname', 'archlinux')}",
            f"  Utilizador:      {c.get('username', '---')}",
            f"  Sudo:            {'Sim' if c.get('sudo') else 'Nao'}",
            f"  Ambiente:        {c.get('desktop', 'gnome')}",
            f"  Driver video:    {c.get('video_driver', 'auto')}",
            f"  Multilib:        {'Sim' if c.get('multilib', True) else 'Nao'}",
            f"  Bootloader:      {c.get('bootloader', 'grub')}",
        ]
        extras = c.get("extra_packages", [])
        if extras:
            lines.append(f"  Extras:          {', '.join(extras)}")

        yield from self.compose_with_sidebar(
            Static("Confirmar Instalacao", id="header-text"),
            Static("Reve as configuracoes abaixo. [Escape] ou [Anterior] para voltar atras e alterar.", classes="help-text"),
            Container(Static("\n".join(lines), id="summary-content"), id="summary-box"),
            Static(
                "ATENCAO: Clicar em INSTALAR vai APAGAR O DISCO e comecar a instalacao.\n"
                "   Esta acao e IRREVERSIVEL.",
                classes="danger-text",
            ),
            Horizontal(
                Button("<- Anterior", id="btn-back", variant="default"),
                Button("INSTALAR", id="btn-install", variant="success"),
                id="nav-buttons",
            ),
        )

    def on_screen_resume(self) -> None:
        self.recompose()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.go_back("desktop")
        elif event.button.id == "btn-install":
            if not self.app.config.get("disk"):
                self.notify("Nenhum disco selecionado.", severity="error")
                return
            self.go_next("installation")

    def action_go_back(self) -> None:
        self.go_back("desktop")
