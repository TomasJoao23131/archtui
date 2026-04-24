from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container, Horizontal


class WelcomeScreen(Screen):
    """Ecrã de boas-vindas — sem sidebar, layout centrado."""

    def compose(self):
        yield Container(
            Static(
                "    ⬡  ArchTUI\n"
                "    ─────────────────────",
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
                "Controlos:\n"
                "  ↑↓    Navegar entre opções\n"
                "  Enter  Confirmar seleção\n"
                "  Tab    Saltar entre campos\n"
                "  q      Sair do instalador",
                id="welcome-keys",
            ),
            Horizontal(
                Button("Iniciar Instalação", id="btn-start", variant="primary"),
                Button("Sair", id="btn-quit", variant="error"),
                id="welcome-buttons",
            ),
            id="welcome-screen",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-start":
            self.app.switch_screen("language")
        elif event.button.id == "btn-quit":
            self.app.exit()
