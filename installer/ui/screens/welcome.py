from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container, Horizontal
from textual.binding import Binding


class WelcomeScreen(Screen):
    """Ecrã de boas-vindas — Enter inicia a instalação."""

    BINDINGS = [
        Binding("enter", "start", "Iniciar", show=False),
        Binding("q", "quit_app", "Sair", show=False),
    ]

    def compose(self):
        yield Container(
            Static(
                "\n"
                "    ⬡  ArchTUI\n"
                "    ─────────────────────\n",
                id="welcome-logo",
            ),
            Static(
                "Bem-vindo ao instalador do Arch Linux!\n\n"
                "Este assistente vai guiá-lo passo a passo na instalação\n"
                "completa do Arch Linux no seu computador.\n\n"
                "Serão 9 passos simples:\n"
                "  Idioma → Teclado → Partições → Sistema Base →\n"
                "  Bootloader → Utilizador → Ambiente → Resumo → Instalar\n\n"
                "Pode voltar atrás em qualquer momento.\n"
                "Nenhuma alteração será feita até confirmar no passo final.",
                id="welcome-text",
            ),
            Static(
                "Controlos:   Enter = Avançar  │  Tab = Navegar  │  q = Sair",
                id="welcome-keys",
            ),
            Horizontal(
                Button("▸ Iniciar Instalação  [Enter]", id="btn-start", variant="primary"),
                Button("  Sair  [q]", id="btn-quit", variant="error"),
                id="welcome-buttons",
            ),
            id="welcome-screen",
        )

    def action_start(self) -> None:
        self.app.switch_screen("language")

    def action_quit_app(self) -> None:
        self.app.exit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-start":
            self.action_start()
        elif event.button.id == "btn-quit":
            self.action_quit_app()
