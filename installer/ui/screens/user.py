from textual.widgets import Static, Button, Input, Switch
from textual.containers import Horizontal
from installer.ui.sidebar import InstallerScreen


class UserScreen(InstallerScreen):
    """Passo 6 — Configuração do utilizador."""

    STEP_NUMBER = 6
    STEP_NAME = "Utilizador"

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Passo 6 — Configuração do Utilizador", id="header-text"),
            Static(
                "Crie a conta de utilizador principal do sistema.\n"
                "Esta será a conta que usa no dia a dia.",
                classes="help-text",
            ),
            Static("Nome de utilizador (sem espaços, minúsculas):", classes="field-label"),
            Input(placeholder="utilizador", id="username-input"),
            Static("Palavra-passe:", classes="field-label"),
            Input(placeholder="", id="password-input", password=True),
            Static("Confirmar palavra-passe:", classes="field-label"),
            Input(placeholder="", id="password-confirm-input", password=True),
            Horizontal(
                Switch(False, id="sudo-switch"),
                Static(
                    "  Conceder privilégios sudo (permite executar comandos como root)",
                    classes="field-label",
                ),
                classes="switch-row",
            ),
            Static(
                "Palavra-passe do root (administrador).\n"
                "Deixe vazio para usar a mesma do utilizador:",
                classes="field-label",
            ),
            Input(placeholder="(mesma do utilizador se vazio)", id="root-password-input", password=True),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            username = self.query_one("#username-input", Input)
            password = self.query_one("#password-input", Input)
            password_confirm = self.query_one("#password-confirm-input", Input)
            root_password = self.query_one("#root-password-input", Input)
            sudo_switch = self.query_one("#sudo-switch", Switch)

            if not username.value.strip():
                self.notify("Indique um nome de utilizador.", severity="warning")
                return

            if " " in username.value:
                self.notify("O nome de utilizador não pode conter espaços.", severity="warning")
                return

            if not password.value:
                self.notify("Indique uma palavra-passe.", severity="warning")
                return

            if len(password.value) < 4:
                self.notify("A palavra-passe deve ter pelo menos 4 caracteres.", severity="warning")
                return

            if password.value != password_confirm.value:
                self.notify("As palavras-passe não coincidem.", severity="error")
                return

            self.app.config["username"] = username.value.strip()
            self.app.config["password"] = password.value
            self.app.config["root_password"] = root_password.value or password.value
            self.app.config["sudo"] = sudo_switch.value
            self.go_next("desktop")

        elif event.button.id == "btn-back":
            self.go_back("bootloader")
