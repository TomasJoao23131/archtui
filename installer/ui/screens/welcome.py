from textual.screen import Screen
from textual.widgets import Static, Button, Checkbox
from textual.containers import Container, Horizontal
from textual.binding import Binding


class WelcomeScreen(Screen):
    """Ecra inicial — Enter ou clique para comecar."""

    BINDINGS = [
        Binding("enter", "start", "Iniciar", show=False),
        Binding("q", "quit_app", "Sair", show=False),
    ]

    def compose(self):
        yield Container(
            Static(
                "\n"
                "            ArchTUI\n"
                "        ---------------------\n"
                "    Instalador do Arch Linux v0.2\n",
                id="welcome-logo",
            ),
            Static(
                "Bem-vindo ao ArchTUI — o instalador guiado do Arch Linux.\n\n"
                "Em 9 passos simples, este assistente configura e instala\n"
                "o Arch Linux no teu computador. Podes usar o teclado\n"
                "ou o rato para navegar. Nenhuma alteracao e feita\n"
                "ate confirmares no passo final.",
                id="welcome-text",
            ),
            Checkbox(
                "Ativar repositorio [multilib]  —  Jogos, Steam e Wine (32-bits)",
                id="multilib-checkbox",
                value=True,
            ),
            Static(
                "Recomendado para a maioria dos utilizadores. Desativa apenas\n"
                "se quiseres um sistema puramente de 64-bits.",
                classes="help-text",
            ),
            Static(
                "NOTA — Ligacao a Internet\n"
                "Este instalador precisa de ligacao a Internet. Se estiveres\n"
                "ligado por cabo Ethernet, ja estas pronto. Se precisares\n"
                "de WiFi, abre outro terminal (Alt+F2) e executa:\n\n"
                "  1. iwctl                         (abrir ferramenta WiFi)\n"
                "  2. station wlan0 scan             (procurar redes)\n"
                "  3. station wlan0 get-networks     (listar redes)\n"
                "  4. station wlan0 connect NOME     (ligar a rede)\n"
                "  5. exit                           (voltar ao terminal)\n\n"
                "Depois volta a este terminal (Alt+F1) e continua.",
                classes="note-box",
            ),
            Static(
                "  Enter  Iniciar    |    q  Sair    |    Mouse  Clicavel",
                id="welcome-keys",
            ),
            Horizontal(
                Button("  Iniciar Instalacao  ", id="btn-start", variant="primary"),
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
