from textual.widgets import Static, Button, OptionList
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
    """Passo 1 — Enter na lista avança automaticamente."""

    STEP_NUMBER = 1
    STEP_NAME = "Idioma"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Passo 1 — Selecionar Idioma", id="header-text"),
            Static(
                "Escolha o idioma do sistema (define locale: datas, números, mensagens).\n"
                "Use ↑↓ para navegar e Enter para confirmar e avançar.",
                classes="help-text",
            ),
            OptionList(*[lang[0] for lang in LANGUAGES], id="language-list"),
            Horizontal(
                Button("← Início", id="btn-back", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Enter na lista = guarda e avança."""
        if event.option_list.id == "language-list":
            idx = event.option_index
            self.app.config["language"] = LANGUAGES[idx][1]
            self.go_next("keyboard")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            idx = self.get_highlighted("#language-list")
            self.app.config["language"] = LANGUAGES[idx][1]
            self.go_next("keyboard")
        elif event.button.id == "btn-back":
            self.app.switch_screen("welcome")

    def action_go_back(self) -> None:
        self.app.switch_screen("welcome")
