from textual.widgets import Static, Button
from textual.binding import Binding
from textual.containers import Container, Horizontal
from installer.ui.sidebar import InstallerScreen


class SummaryScreen(InstallerScreen):
    STEP_NUMBER = 8
    STEP_NAME = "Resumo"
    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def compose(self):
        c = self.app.config
        lines = [
            f"  Idioma:       {c.get('language', 'pt_BR')}",
            f"  Teclado:      {c.get('keyboard', 'br-abnt2')}",
            f"  Disco:        {c.get('disk_label', '—')}",
            f"  Hostname:     {c.get('hostname', 'archlinux')}",
            f"  Utilizador:   {c.get('username', '—')}",
            f"  Sudo:         {'Sim' if c.get('sudo') else 'Não'}",
            f"  Ambiente:     {c.get('desktop', 'gnome')}",
            f"  Driver:       {c.get('video_driver', 'auto')}",
            f"  Multilib:     {'Sim' if c.get('multilib', True) else 'Não'}",
            f"  Bootloader:   {c.get('bootloader', 'grub')}",
        ]
        extras = c.get("extra_packages", [])
        if extras:
            lines.append(f"  Extras:       {', '.join(extras)}")

        yield from self.compose_with_sidebar(
            Static("Passo 8 — Resumo", id="header-text"),
            Static("Reveja tudo. Escape para voltar.", classes="help-text"),
            Container(Static("\n".join(lines), id="summary-content"), id="summary-box"),
            Static("⚠  INSTALAR apaga o disco. IRREVERSÍVEL.", classes="danger-text"),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("✓ INSTALAR", id="btn-install", variant="success"),
                id="nav-buttons",
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.go_back("desktop")
        elif event.button.id == "btn-install":
            if not self.app.config.get("disk"):
                self.notify("Sem disco selecionado.", severity="error")
                return
            self.go_next("installation")

    def action_go_back(self) -> None:
        self.go_back("desktop")
