from textual.widgets import Static, Button, OptionList
from textual.containers import Horizontal
from installer.ui.sidebar import InstallerScreen


LANGUAGES = [
    ("Português (Brasil)", "pt_BR"),
    ("Português (Portugal)", "pt_PT"),
    ("English (US)", "en_US"),
    ("Español", "es_ES"),
]


class LanguageScreen(InstallerScreen):
    """Passo 1 — Seleção do idioma do sistema."""

    STEP_NUMBER = 1
    STEP_NAME = "Idioma"

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Passo 1 — Selecionar Idioma", id="header-text"),
            Static(
                "Escolha o idioma que será configurado no sistema instalado.\n"
                "Isto define o locale (formato de datas, números e mensagens do sistema).",
                classes="help-text",
            ),
            OptionList(*[lang[0] for lang in LANGUAGES], id="language-list"),
            Horizontal(
                Button("← Início", id="btn-back", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            option_list = self.query_one("#language-list", OptionList)
            idx = option_list.highlighted if option_list.highlighted is not None else 0
            self.app.config["language"] = LANGUAGES[idx][1]
            self.go_next("keyboard")
        elif event.button.id == "btn-back":
            self.app.switch_screen("welcome")
