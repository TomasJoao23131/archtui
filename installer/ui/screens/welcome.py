from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container, Horizontal
from textual.binding import Binding


class WelcomeScreen(Screen):
    """Ecrã inicial — Enter ou clique para começar."""

    BINDINGS = [
        Binding("enter", "start", "Iniciar", show=False),
        Binding("q", "quit_app", "Sair", show=False),
    ]

    def compose(self):
        yield Container(
            Static(
                "\n"
                "     ⬡  ArchTUI\n"
                "     ─────────────────\n",
                id="welcome-logo",
            ),
            Static(
                "Instalador do Arch Linux com interface gráfica.\n\n"
                "9 passos simples para instalar o Arch Linux.\n"
                "Pode usar o rato ou o teclado para navegar.\n"
                "Nenhuma alteração é feita até ao passo final.",
                id="welcome-text",
            ),
            Static(
                "[Enter] Iniciar  │  [q] Sair  │  [Mouse] Clicável",
                id="welcome-keys",
            ),
            Horizontal(
                Button("Iniciar Instalação", id="btn-start", variant="primary"),
                Button("Sair", id="btn-quit", variant="error"),
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
