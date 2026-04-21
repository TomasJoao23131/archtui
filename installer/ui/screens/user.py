from textual.widgets import Static, Button, Input, Switch
from textual.containers import Container, Horizontal
from installer.ui.sidebar import InstallerScreen


class UserScreen(InstallerScreen):
    STEP_NUMBER = 6
    STEP_NAME = "Utilizador"

    def compose(self):
        content = Container(
            Static("Configurar Utilizador", id="header-text"),
            Static("Nome do utilizador:", id="username-label"),
            Input(placeholder="usuario", id="username-input"),
            Static("Palavra-passe:", id="password-label"),
            Input(placeholder="", id="password-input", type="password"),
            Static("Confirmar palavra-passe:", id="password-confirm-label"),
            Input(placeholder="", id="password-confirm-input", type="password"),
            Switch(False, id="sudo-switch"),
            Static("Conceder privilegios sudo ao utilizador", id="sudo-label"),
            Static("Root password (deixe vazio para usar a mesma):", id="root-label"),
            Input(placeholder="", id="root-password-input", type="password"),
            Horizontal(
                Button("Anterior", id="btn-back", variant="default"),
                Button("Seguinte", id="btn-next", variant="primary"),
                id="nav-buttons"
            ),
            id="user-container"
        )
        yield from self.compose_with_sidebar(content)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            username = self.query_one("#username-input", Input)
            password = self.query_one("#password-input", Input)
            password_confirm = self.query_one("#password-confirm-input", Input)
            root_password = self.query_one("#root-password-input", Input)
            sudo_switch = self.query_one("#sudo-switch", Switch)

            if not username.value:
                self.notify("Indica um nome de utilizador.", severity="warning")
                return

            if not password.value:
                self.notify("Indica uma palavra-passe.", severity="warning")
                return

            if password.value != password_confirm.value:
                self.notify("As palavras-passe nao coincidem.", severity="error")
                return

            self.app.config["username"] = username.value
            self.app.config["password"] = password.value
            self.app.config["root_password"] = root_password.value or password.value
            self.app.config["sudo"] = sudo_switch.value
            self.app.push_screen("desktop")
        elif event.button.id == "btn-back":
            self.app.pop_screen()
