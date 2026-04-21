from textual.widgets import Static, Button
from textual.containers import Container, Horizontal
from installer.ui.sidebar import InstallerScreen


class WelcomeScreen(InstallerScreen):
    def compose(self):
        content = Container(
            Static("ArchTUI - Instalador do Arch Linux", id="title"),
            Static(
                "Bem-vindo ao instalador do Arch Linux!\n\n"
                "Este assistente vai guia-lo passo a passo na instalacao\n"
                "do Arch Linux no seu sistema.\n\n"
                "Navegacao:\n"
                "  - Use as setas para navegar\n"
                "  - Enter para confirmar\n"
                "  - Tab para mudar entre elementos\n"
                "  - q para sair\n\n"
                "Clique em 'Iniciar Instalacao' para comecar.",
                id="welcome-text"
            ),
            Horizontal(
                Button("Iniciar Instalacao", id="btn-start", variant="primary"),
                Button("Sair", id="btn-quit", variant="error"),
                id="buttons"
            ),
            id="welcome-container"
        )
        yield from self.compose_with_sidebar(content)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-start":
            self.app.push_screen("language")
        elif event.button.id == "btn-quit":
            self.app.quit()
