from textual.widgets import Static, Button, Input, Switch
from textual.containers import Horizontal
from textual.binding import Binding
from installer.ui.sidebar import InstallerScreen


class UserScreen(InstallerScreen):
    """Passo 6 — Dados do utilizador."""

    STEP_NUMBER = 6
    STEP_NAME = "Utilizador"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Passo 6 — Utilizador", id="header-text"),
            Static(
                "Crie a conta principal. Tab para navegar entre campos.",
                classes="help-text",
            ),
            Static("Nome de utilizador:", classes="field-label"),
            Input(placeholder="utilizador", id="username-input"),
            Static("Palavra-passe:", classes="field-label"),
            Input(placeholder="", id="password-input", password=True),
            Static("Confirmar palavra-passe:", classes="field-label"),
            Input(placeholder="", id="password-confirm-input", password=True),
            Horizontal(
                Switch(True, id="sudo-switch"),
                Static("  Conceder sudo (recomendado)", classes="field-label"),
                classes="switch-row",
            ),
            Static("Password root (vazio = mesma):", classes="field-label"),
            Input(placeholder="(mesma do utilizador)", id="root-password-input", password=True),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            self._try_advance()
        elif event.button.id == "btn-back":
            self.go_back("bootloader")

    def _try_advance(self) -> None:
        username = self.query_one("#username-input", Input).value.strip()
        password = self.query_one("#password-input", Input).value
        confirm = self.query_one("#password-confirm-input", Input).value
        root_pw = self.query_one("#root-password-input", Input).value
        sudo = self.query_one("#sudo-switch", Switch).value

        if not username:
            self.notify("Indique um nome de utilizador.", severity="warning")
            return
        if " " in username:
            self.notify("Sem espaços no nome de utilizador.", severity="warning")
            return
        if not password:
            self.notify("Indique uma palavra-passe.", severity="warning")
            return
        if password != confirm:
            self.notify("As palavras-passe não coincidem.", severity="error")
            return

        self.app.config["username"] = username
        self.app.config["password"] = password
        self.app.config["root_password"] = root_pw or password
        self.app.config["sudo"] = sudo
        self.go_next("desktop")

    def action_go_back(self) -> None:
        self.go_back("bootloader")
