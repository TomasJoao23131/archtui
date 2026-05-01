import re
from textual.widgets import Static, Button, Input, Switch, Checkbox, RadioSet, RadioButton
from textual.containers import Horizontal
from textual.binding import Binding
from installer.ui.sidebar import InstallerScreen

RESERVED_NAMES = {"root", "nobody", "daemon", "bin", "sys", "sync", "games",
                  "man", "lp", "mail", "news", "uucp", "proxy", "www-data",
                  "backup", "list", "irc", "gnats", "systemd-network",
                  "systemd-resolve", "messagebus", "sshd"}

SHELLS = [
    ("Bash (Padrão)", "bash"),
    ("Zsh (Recomendado)", "zsh"),
    ("Fish (Moderno)", "fish"),
]


class UserScreen(InstallerScreen):
    STEP_NUMBER = 6
    STEP_NAME = "Utilizador"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Configuração do Utilizador", id="header-text"),
            Static("Cria a tua conta principal. Usa [Tab] para mudar de campo.", classes="help-text"),
            Static("Nome de utilizador (sem espaços, minúsculas):", classes="field-label"),
            Input(placeholder="utilizador", id="username-input"),
            Static("Palavra-passe:", classes="field-label"),
            Input(placeholder="Palavra-passe...", id="password-input", password=True),
            Static("Confirmar palavra-passe:", classes="field-label"),
            Input(placeholder="Repetir palavra-passe...", id="password-confirm-input", password=True),
            Checkbox("Mostrar palavras-passe", id="show-password-checkbox"),
            Static("Shell padrão:", classes="field-label"),
            RadioSet(
                *[RadioButton(s[0], id=f"shell-{i}") for i, s in enumerate(SHELLS)],
                id="shell-list",
            ),
            Horizontal(
                Switch(True, id="sudo-switch"),
                Static("  Conceder privilégios sudo (recomendado)", classes="field-label"),
                classes="switch-row",
            ),
            Static("Palavra-passe root (deixa vazio para usar a mesma do utilizador):", classes="field-label"),
            Input(placeholder="(mesma do utilizador se vazio)", id="root-password-input", password=True),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_mount(self):
        try:
            self.query_one("#shell-0", RadioButton).value = True
        except Exception:
            pass

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        if event.checkbox.id == "show-password-checkbox":
            show = event.value
            for input_id in ("password-input", "password-confirm-input", "root-password-input"):
                try:
                    inp = self.query_one(f"#{input_id}", Input)
                    inp.password = not show
                except Exception:
                    pass

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

        # Validacao do username
        if not username:
            self.notify("Indique um nome de utilizador.", severity="warning")
            return
        if len(username) > 32:
            self.notify("O nome de utilizador nao pode ter mais de 32 caracteres.", severity="warning")
            return
        if not re.match(r'^[a-z_][a-z0-9_-]*$', username):
            self.notify(
                "Nome invalido. Use apenas minusculas, numeros, - e _.\n"
                "Deve comecar por uma letra ou _.",
                severity="warning",
            )
            return
        if username in RESERVED_NAMES:
            self.notify(f"'{username}' e um nome reservado do sistema.", severity="error")
            return

        # Validacao da password
        if not password:
            self.notify("Indique uma palavra-passe.", severity="warning")
            return
        if len(password) < 4:
            self.notify("A palavra-passe deve ter pelo menos 4 caracteres.", severity="warning")
            return
        if password != confirm:
            self.notify("As palavras-passe nao coincidem.", severity="error")
            return

        shell_idx = self.get_radio_index("#shell-list")
        shell = SHELLS[shell_idx][1]

        self.app.config["username"] = username
        self.app.config["password"] = password
        self.app.config["root_password"] = root_pw or password
        self.app.config["sudo"] = sudo
        self.app.config["shell"] = shell
        self.go_next("desktop")

    def action_go_back(self) -> None:
        self.go_back("bootloader")

