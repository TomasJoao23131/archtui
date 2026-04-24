from textual.widgets import Static, Button, RadioSet, RadioButton
from textual.containers import Horizontal
from textual.binding import Binding
from installer.ui.sidebar import InstallerScreen


LANGUAGES = [
    ("Português (Brasil)", "pt_BR"),
    ("Português (Portugal)", "pt_PT"),
    ("English (US)", "en_US"),
    ("Español", "es_ES"),
]


class LanguageScreen(InstallerScreen):
    STEP_NUMBER = 1
    STEP_NAME = "Idioma"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Idioma do sistema", id="header-text"),
            Static(
                "Escolha o idioma que será configurado no sistema instalado.\n"
                "Isto define o locale (formato de datas, números e mensagens).",
                classes="help-text",
            ),
            RadioSet(
                *[RadioButton(lang[0], id=f"lang-{i}") for i, lang in enumerate(LANGUAGES)],
                id="language-list",
            ),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_mount(self):
        # Selecionar o primeiro por defeito
        self.query_one("#lang-0", RadioButton).value = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            idx = self.get_radio_index("#language-list")
            self.app.config["language"] = LANGUAGES[idx][1]
            self.go_next("keyboard")
        elif event.button.id == "btn-back":
            self.app.switch_screen("welcome")

    def action_go_back(self) -> None:
        self.app.switch_screen("welcome")
