from textual.screen import Screen
from textual.widgets import Static, Button, Checkbox
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
                "            ⬡  ArchTUI\n"
                "        ─────────────────────\n"
                "    Instalador do Arch Linux v0.1\n",
                id="welcome-logo",
            ),
            Static(
                "Bem-vindo ao ArchTUI — o instalador guiado do Arch Linux.\n\n"
                "Em 9 passos simples, este assistente configura e instala\n"
                "o Arch Linux no teu computador. Podes usar o teclado\n"
                "ou o rato para navegar. Nenhuma alteração é feita\n"
                "até confirmares no passo final.",
                id="welcome-text",
            ),
            Checkbox(
                "Ativar repositório [multilib]  ─  Jogos, Steam e Wine (32-bits)",
                id="multilib-checkbox",
                value=True,
            ),
            Static(
                "Recomendado para a maioria dos utilizadores. Desativa apenas\n"
                "se quiseres um sistema puramente de 64-bits.",
                classes="help-text",
            ),
            Static(
                "  Enter  Iniciar    │    q  Sair    │    Mouse  Clicável",
                id="welcome-keys",
            ),
            Horizontal(
                Button("  Iniciar Instalação  ", id="btn-start", variant="primary"),
                Button("  Sair  ", id="btn-quit", variant="error"),
                id="welcome-buttons",
            ),
            id="welcome-screen",
        )

    def action_start(self) -> None:
        try:
            chk = self.query_one("#multilib-checkbox", Checkbox)
            self.app.config["multilib"] = chk.value
        except Exception:
            pass
        self.app.switch_screen("language")

    def action_quit_app(self) -> None:
        self.app.exit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-start":
            self.action_start()
        elif event.button.id == "btn-quit":
            self.action_quit_app()
